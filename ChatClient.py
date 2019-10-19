import eel
import mysql.connector
import errno
import sys

# Logica de cliente


import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

nombre_socket = socket.socket()

try:
    bandera = True
    nombre_socket.connect((HOST, PORT))
except  ConnectionRefusedError:
    bandera = False

eel.init('web')

config = {
    'user': 'root',
    'password': '',
    # 'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'chat',
    'raise_on_warnings': True,
}
link = mysql.connector.connect(**config)


@eel.expose
def add_user(name, image):
    my_cursor = link.cursor()
    sql = "INSERT INTO users (name, image) VALUES (%s, %s)"
    val = (name, image)
    my_cursor.execute(sql, val)
    eel.setUserId(my_cursor.lastrowid)
    link.commit()


@eel.expose
def get_users():
    my_cursor = link.cursor()
    sql = "SELECT * FROM users ORDER BY id DESC"
    my_cursor.execute(sql)
    users = [dict(name=row[1], image=row[2], lastMessage=get_last_message(row[0])) for row in my_cursor.fetchall()]
    eel.getUsers(users)
    get_messages()


def get_last_message(user):
    my_cursor = link.cursor()
    sql = "SELECT * FROM posts WHERE user_id = %s ORDER BY id DESC LIMIT 1"
    my_cursor.execute(sql, (user,))
    for row in my_cursor.fetchall():
        return row[1]


def get_messages():
    my_cursor = link.cursor()
    sql = "SELECT * FROM posts"
    my_cursor.execute(sql)
    messages = [dict(user=row[2], message=row[1], id=row[0]) for row in my_cursor.fetchall()]
    eel.getMessages(messages)


@eel.expose
def add_message(message, user_id):
    my_cursor = link.cursor()
    sql = "INSERT INTO posts (message, user_id) VALUES (%s,%s)"
    val = (message, user_id)
    my_cursor.execute(sql, val)
    nombre_socket.send(message.encode())
    link.commit()


def send_message_to_email(message):
    email = 'fabianportillo97@gmail.com'


eel.start('index.html', size=(1076, 651))

#     while True:
#
#         # Wait for user to input a message
#         message = input(f'{my_username} > ')
#
#         # If message is not empty - send it
#         if message:
#             # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
#             message = message.encode('utf-8')
#
#             client_socket.send(message_header + message)
#
#         try:
#             # Now we want to loop over received messages (there might be more than one) and print them
#             while True:
#
#                 # Receive our "header" containing username length, it's size is defined and constant
#                 username_header = client_socket.recv(HEADER_LENGTH)
#
#                 # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
#                 if not len(username_header):
#                     print('Connection closed by the server')
#                     sys.exit()
#
#                 # Convert header to int value
#                 username_length = int(username_header.decode('utf-8').strip())
#
#                 # Receive and decode username
#                 username = client_socket.recv(username_length).decode('utf-8')
#
#                 # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
#                 message_header = client_socket.recv(HEADER_LENGTH)
#                 message_length = int(message_header.decode('utf-8').strip())
#                 message = client_socket.recv(message_length).decode('utf-8')
#
#                 # Print message
#                 print(f'{username} > {message}')
#
#         except IOError as e:
#             # This is normal on non blocking connections - when there are no incoming data error is going to be raised
#             # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
#             # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
#             # If we got different error code - something happened
#             if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
#                 print('Reading error: {}'.format(str(e)))
#                 sys.exit()
#
#             # We just did not receive anything
#             continue
#
#         except Exception as e:
#             # Any other exception - something happened, exit
#             print('Reading error: '.format(str(e)))
#             sys.exit()
