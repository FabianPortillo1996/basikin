import eel
import mysql.connector
import socket

s = socket.socket()  # Create a socket object
s.connect(('192.168.0.5', 1234))
# s.sendall('Here I am!'.encode())
# s.close()

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
    link.commit()


def send_message_to_email(message):
    email = 'fabianportillo97@gmail.com'


eel.start('index.html', size=(1000, 600))
