# analyze_traces.py
import json
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans

# load traces (file you uploaded)
with open('collected_data.txt','r') as f:
    data = json.load(f)   # expects JSON array of traces

# normalize -> list of lists of ints
traces = [list(t) for t in data]
n_traces = len(traces)
lengths = [len(t) for t in traces]
print("num traces:", n_traces, "lengths stats:", min(lengths), max(lengths))

# choose a set of traces (or all) and trim to minimal length
L = min(lengths)
T = np.array([t[:L] for t in traces], dtype=np.float32)  # shape (n_traces, L)

# quick plot first few traces
import matplotlib.pyplot as plt
plt.figure(figsize=(10,4))
for i in range(min(6, n_traces)):
    plt.plot(T[i,:], alpha=0.7, label=f"trace{i}")
plt.legend(); plt.title("Sample traces (first 6)"); plt.show()

# For each time index (column), try to cluster values into 2 groups (add/no-add)
# We'll record classification confidence and majority vote per column.
cols = T.shape[1]
col_votes = np.zeros(cols, dtype=int)
col_conf = np.zeros(cols, dtype=float)

for j in range(cols):
    col = T[:, j].reshape(-1,1)
    # try Gaussian Mixture with 2 components
    try:
        g = GaussianMixture(n_components=2, covariance_type='full', random_state=0)
        g.fit(col)
        labels = g.predict(col)
        # determine which label corresponds to "higher" mean
        means = [col[labels==k].mean() if (labels==k).sum()>0 else -1 for k in (0,1)]
        # define bit=1 if sample belongs to cluster with larger mean (heuristic)
        cluster_for_add = int(np.argmax(means))
        votes = (labels == cluster_for_add).astype(int)
        col_votes[j] = int(votes.sum() > (n_traces/2))  # majority
        # confidence = abs(diff in cluster sizes) / n_traces
        col_conf[j] = abs(votes.sum() - (n_traces - votes.sum())) / n_traces
    except Exception as e:
        col_votes[j] = 0
        col_conf[j] = 0.0

# show a compact visualization of votes
plt.figure(figsize=(12,2))
plt.imshow(col_votes.reshape(1,-1), aspect='auto', cmap='Greys', interpolation='nearest')
plt.title('Guessed add(black=1) / no-add(white=0) per sample index'); plt.yticks([])
plt.show()

# The double-and-add loop emits two events per bit (double, optional add).
# We need to group the columns into bit-steps: try to detect repeating pattern length,
# e.g., find periodicity by autocorrelation of col_conf or col_votes.
ac = np.correlate(col_conf - col_conf.mean(), col_conf - col_conf.mean(), mode='full')
ac = ac[ac.size//2:]
# find first significant peak > 0 (ignoring lag=0)
lags = np.arange(len(ac))
peaks = np.where(ac > 0.2 * ac.max())[0]
print("Autocorr peaks (candidate periods):", peaks[:10])

# Heuristic: pick a period p (if exists)
if len(peaks) >= 2:
    period = peaks[1]  # second peak often indicates period
    print("Heuristic period:", period)
else:
    period = None
    print("No clear period found; will try grouping by 2-sample per bit.")

# If no clear period, assume pattern 2 samples per bit (double, add slot)
if period is None or period < 2:
    # group into bit slots of size 2
    slot_size = 2
else:
    slot_size = period

num_bits = cols // slot_size
print("Assuming slot_size", slot_size, "=> num_bits", num_bits)

# For each bit i, aggregate votes in that slot (majority -> bit)
bits = []
conf_bits = []
for i in range(num_bits):
    s = i*slot_size
    e = s + slot_size
    slot_votes = col_votes[s:e]
    slot_conf = col_conf[s:e]
    # decide bit: majority of votes in slot
    bit = int(slot_votes.sum() > (slot_size/2))
    bits.append(bit)
    conf_bits.append(slot_conf.mean())

print("Recovered bits (first 100):", bits[:100])
print("Confidence per bit (avg):", np.mean(conf_bits))

# convert bits (assume MSB->LSB) to int:
n = 0
for b in bits:
    n = (n << 1) | b
print("Recovered integer (hex):", hex(n))

# Save results
with open('recovered_bits.json','w') as f:
    json.dump({"bits": bits, "conf": conf_bits, "n": n}, f)
print("Saved recovered_bits.json")
