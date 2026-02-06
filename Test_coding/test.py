import socket
import random

HOST = "0.0.0.0"
PORT = 12345

money = 100

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print("Tai Xiu server running...")
conn, addr = s.accept()

conn.sendall(b"Welcome Tai Xiu! Ban co 100$\nNhap: tai|xiu so_tien  (vd: tai 20)\n")

while True:
    data = conn.recv(1024)
    if not data:
        break

    msg = data.decode().strip().lower()
    if msg == "exit":
        break

    try:
        choice, bet = msg.split()
        bet = int(bet)

        if bet <= 0 or bet > money:
            conn.sendall(f"Tien khong hop le. So du: {money}$\n".encode())
            continue

        dice = [random.randint(1,6) for _ in range(3)]
        total = sum(dice)
        result = "tai" if total >= 11 else "xiu"

        if choice == result:
            money += bet
            outcome = "WIN"
        else:
            money -= bet
            outcome = "LOSE"

        reply = (
            f"Xuc xac: {dice} | Tong: {total} ({result.upper()})\n"
            f"{outcome}! So du: {money}$\n"
        )

        if money <= 0:
            reply += "GAME OVER\n"
            conn.sendall(reply.encode())
            break

        conn.sendall(reply.encode())

    except:
        conn.sendall(b"Nhap sai dinh dang! (tai|xiu so_tien)\n")

conn.close()
s.close()
