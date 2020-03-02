import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.193", 1234)) #Change IP to the server IP

while True:
    msg = s.recv(1)
    print(msg.decode("utf-8"))