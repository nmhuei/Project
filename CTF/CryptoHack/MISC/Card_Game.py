from Crypto.Util.number import*
from pwn import*
import json, sys
context.log_level = 'debug'

FLAG = 'crypto{?????????????????????????????}'
VALUES = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
SUITS = ['Clubs', 'Hearts', 'Diamonds', 'Spades']

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return VALUES.index(self.value) > VALUES.index(other.value)

deck = [Card(value, suit) for suit in SUITS for value in VALUES]

def card_index(card, d=deck):
    value, suit = card.split(" of ")
    for i, card in enumerate(deck):
        if card.value == value and card.suit == suit:
            return i
        
        
def unrebase(n, b=52):
    x = 0
    for i in range(len(n)):
        x += n[i] * (52 ** i)
        
    return x

def rebase(n, b=52):
        if n < b:
            return [n]
        else:
            return [n % b] + rebase(n//b, b)

def find_params(x1, x2, x3, m = 2**61 -1):
    mul = (x3 - x2) * inverse(x2 - x1, m) % m
    inc = (x2 - x1 * mul) % m
    
    return mul, inc

def predict_next(X, mul, inc, m =2**61 - 1):
    return (X * mul + inc) % m

def send_choice(s):
    r.send(json.dumps({"choice": s}).encode())
    return json.loads(r.recvline().decode())

def play_11_round_check():
    n = []
    while True:
        res = send_choice('l')
        hand_card = res["hand"]
        n.append(card_index(hand_card))
        if 'reshuffle' in res["msg"]:
            return unrebase(n[::-1])
        
        

r = remote("socket.cryptohack.org", 13383)
res = json.loads(r.recvline().decode())
n1 = card_index(res["hand"])

x1 = play_11_round_check() + n1 * (52**10)
x2 = play_11_round_check()
x3 = play_11_round_check()

x_pre = x3   
mul, inc = find_params(x1, x2, x3)
m = 2**61 - 1

assert (x1 * mul + inc) % m == x2
assert (x2 * mul + inc) % m == x3

k = rebase(x3)
print(k)
hand_card = deck[k[0]]
while True:
    x_next = predict_next(x_pre, mul, inc)
    k = rebase(x_next)
    
    for i in range(len(k)-1, -1, -1):
        hidden_card = deck[k[i]]
        
        if hidden_card > hand_card:
            send_choice('h')
        else:
            send_choice('l')
            
        hand_card = hidden_card
    
    x_pre = x_next