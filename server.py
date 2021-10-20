"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain

server.py
"""

from socket import *
from random import *
import selectors
import signal

# Selectors
sel = selectors.DefaultSelector()


# Function signalHandler handles user interrupt ^C
def signalHandler(sig, frame):
    # Print interrupt message
    print("Interrupt received, shutting down ...")
    discMsg = "DISCONNECT CHAT/1.0"
    # Iterate through the client dictionary
    for i in clientDict:
        # Send disconnect message, unregister and close connection
        i.send(discMsg.encode())
        sel.unregister(i)
        i.close()
    exit()


# handle function handles the initial call
def handle(conn, mask):
    # Tries to receive the message
    try:
        conn, addr = serverSocket.accept()
        sel.register(conn, selectors.EVENT_READ, readMessage)
    # Catches errors from accept() or register()
    except (BlockingIOError, InterruptedError, ConnectionAbortedError, ValueError, KeyError):
        pass


# checkRegistration function checks the registration of the new connection
def checkRegistration(conn, message):
    # The split command is put into a try and exceptions are caught
    try:
        (reg, client, chat) = message.split(" ")
    except ValueError:
        # Print and send 400 Invalid registration
        print("400 Invalid registration")
        conn.send("400 Invalid registration".encode())

    # Valid message that can be compared with the received message
    validMessage = "REGISTER " + client + " CHAT/1.0"

    # Check format of registration message and presence of username in list
    if message == validMessage:

        # Checks if it's a unique username
        if client not in clientDict.values():

            # Include the socket in the socket list
            socketList.append(conn)
            # Include the client in the dictionary
            clientDict[conn] = client
            # Send the success message
            conn.send("200 Registration successful".encode())
            clientDetails = conn.recv(1024).decode()
            print("Accepted connection from client address: " + str(clientDetails))
            # Print the accepted connection details
            print("Connection to client established, waiting to receive messages from user '" + client + "' ...")
        # Client already exists, send error message
        else:
            # Print to server and send to attempting connection that the client name exists
            conn.send("401 Client already registered".encode())
            # Unregister and close connection
            sel.unregister(conn)
            conn.close()

    # Error with message format
    else:
        # Print to server and send to attempting connection that the registration is invalid
        print("400 Invalid registration")
        conn.send("400 Invalid registration".encode())
        # Unregister and close connection
        sel.unregister(conn)
        conn.close()


# Function
def readMessage(conn, eventMask):
    # Read message
    message = conn.recv(1024).decode()
    if message:
        # If the socket does not exist in our list check the registration message
        if conn not in socketList:
            checkRegistration(conn, message)
        else:
            user = clientDict[conn]
            # Check if it's a disconnect message
            if message == "DISCONNECT " + user + " CHAT/1.0":
                print("Disconnecting user " + user)
                # Remove the receiveSocket (key) and the client (item) from the dictionary
                clientDict.pop(conn)
                # Remove the socket from the socket list, unregister, and close connection
                socketList.remove(conn)
                sel.unregister(conn)
                conn.close()
            else:
                # Print the received message
                print("Received message from user " + clientDict[conn] + ": " + message)
                # Broadcast message to all clients except the sender
                for clientSocket in clientDict:
                    if clientSocket != conn:
                        clientSocket.send(message.encode())
    else:
        sel.unregister(conn)
        conn.close()


# Server Port, and Address
serverPort = randrange(5000, 12000)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
sel.register(serverSocket, selectors.EVENT_READ, handle)

# List of sockets
socketList = []
# Dictionary containing sockets and the clients
clientDict = {}

# Print statements indicating that the server is waiting for clients on a particular port
print('Will wait for client connections at port', serverPort)
print('Waiting for incoming client connections ...')

while True:
    # Checks for user interrupt --> ^C
    signal.signal(signal.SIGINT, signalHandler)

    # Selectors
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
