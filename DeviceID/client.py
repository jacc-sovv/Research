import socket
import uuid
import subprocess
import os

def get_id():
    if 'nt' in os.name:
        id = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
        return id
    else:
        id = str(subprocess.check_output(['cat', '/etc/machine-id']), 'utf-8')
        return id

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def length_of_message(message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length, message

def first_send(msg):
    id = get_id()
    id_length, id_msg = length_of_message(id)   
    client.send(id_length)
    client.send(id_msg)
    print(client.recv(2048).decode(FORMAT)) #Why 2048? Well, we know the server msg will be "msg recieved" always, so size is not an issue
    send_length, message = length_of_message(msg)
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def send(msg):
    send_length, message = length_of_message(msg)
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

#To test what happens if you're device is not listed
def bad_send(msg):
    id = "123"
    id_length, id_msg = length_of_message(id)   
    client.send(id_length)
    client.send(id_msg)
    print(client.recv(2048).decode(FORMAT))
    send_length, message = length_of_message(msg)
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

#Press enter in the terminal running client to send next message. These are placeholder messages.
first_send("Hello World!")
input()
send("Testing testing 123")
input()
send("It's me, smormi!")

send(DISCONNECT_MESSAGE)