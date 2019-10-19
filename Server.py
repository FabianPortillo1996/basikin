#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

nombre_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nombre_socket.bind((HOST, PORT))

nombre_socket.listen(20)

id_socket_cliente, direccion = nombre_socket.accept()

while True:
    bytes_a_recibir = 1024
    mensaje_recibido = id_socket_cliente.recv(bytes_a_recibir)
    texto = mensaje_recibido.decode("utf-8")
    id_socket_cliente.send(texto.encode())
    if texto == 'Ya no mas':
        break
    else:
        print(texto)

id_socket_cliente.close()
nombre_socket.close()
