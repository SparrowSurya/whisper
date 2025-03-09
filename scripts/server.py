import socket

HOST = "127.0.0.1"
PORT = 50_005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print(f"Listening on {HOST}:{PORT}")

c, a = s.accept()
print(f"Accepted: {a}")

input("Press <Enter> key to close ")

c.close()
s.close()
print("Exited")
