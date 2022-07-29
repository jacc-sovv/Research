# Research
# This README is still a work in progress, will be updated throughout the day!

## What is DeviceID
In short, it's a simple client-server program using python sockets to create a proof-of-concept of sending a device ID of a client over to a server, and the server  
authenticating or dropping the connection based on this.

## How it works
The client connects to the server. The server maintains a flag for each client connection on whether or not this is the first message the client sends. If it is the first message,  
the protocol gurantees that the first message sent will be the client's deviceID. The server checks this message, and grants / denies connection based on whether
or not the ID is valid. It only needs to do this once per connection. The server uses multi-threading to allow multiple clients to connect at the same time.  


## How to use deviceID.py:

1) Clone the github repo
2) 
