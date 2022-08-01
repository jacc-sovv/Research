# Research
# This README is still a work in progress, will be updated throughout the day!

## What is DeviceID
In short, it's a simple client-server program using python sockets to create a proof-of-concept of sending a device ID of a client over to a server, and the server  
authenticating or dropping the connection based on this.

## How it works
The client connects to the server. The server maintains a flag for each client connection on whether or not this is the first message the client sends. If it is the first message,  
the protocol gurantees that the first message sent will be the client's deviceID. The server checks this message, and grants / denies connection based on whether
or not the ID is valid. It only needs to do this once per connection. The server uses multi-threading to allow multiple clients to connect at the same time. The client sends messages which can be of any length, and to ensure no overflows the messages first send their length. 


## How to use deviceID.py:

1) Clone the github repo
2) Have two terminal instances open
3) CD into directory of DeviceID folder
4) Begin the server using python3 ./server.py  
4a) The server uses localhost on port 5050 to communicate with the client. This can be adjusted by changing the PORT and SERVER variables in client.py and server.py
5) The client sends messages after the user hits the enter button at the moment. This is to make it clear to both the client and server that a message was sent.
6) The client sends 3 messages and then disconnects  
6a) The disconnect message is !DISCONNECT. The messages are hard-coded, but can be adjusted. They can be of any size, since the protocol sends the message size as a header.
7) Close the server terminal to shut down the server

# Planned updates:
Wrap the sending part of the client in a general "start" function, to ensure that the ID is sent once rather than having to call a separate function for the first connection to the server.

Allow keyboard interrupts to shut down the server rather than closing the terminal.
