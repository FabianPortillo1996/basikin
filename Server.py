import threading
import socket

s = socket.socket()
s.bind(('192.168.0.5', 1234))

s.listen(5)
while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    print(c.recv(1024))
    s.send(c)
    c.close()
