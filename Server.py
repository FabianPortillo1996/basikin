#!/usr/bin/env python3

import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

nombre_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nombre_socket.bind((HOST, PORT))

nombre_socket.listen(20)

clients = []


def recv(clientsocket):
    while True:
        msg = clientsocket.recv(1024)
        for c in clients:
            c.send(msg)


while True:
    c, addr = nombre_socket.accept()
    clients.append(c)
    thread_recv = threading.Thread(target=recv, args=((c,)))
    thread_recv.start()

id_socket_cliente.close()
nombre_socket.close()
