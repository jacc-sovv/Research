import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
VALID_IDS = ["311342B1-1E75-5B9F-BE28-3B28BD6850A7"]        #<-That's my ID! Can add your own to get valid connection
                                                            #check id.py to get your own ID

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def length_of_message(message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length, message

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    first_connection = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if first_connection == True:
                if msg not in VALID_IDS:
                    conn.send("Error: unauthenticated device".encode(FORMAT)) 
                    connected = False
                    break
                else:
                    first_connection = False    #Valid ID!
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    print(f"Disconnecting from {addr}")
    conn.close()
    return
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except KeyboardInterrupt:
            thread.join()
            if conn:
                conn.close()
            break


print("[STARTING] server is starting...")
start()