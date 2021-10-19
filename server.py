"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
import socket
from random import *
from socket import *
import signal
import select


# Functions to assist with the program

# Function signalHandler handles user interrupt ^C
def signalHandler(sig, frame):
    print("Interrupt received, shutting down ...")
    discMsg = "DISCONNECT CHAT/1.0"
    # Send each client the disconnect message
    for i in clientList:
        i.send(discMsg.encode())
    exit()


# Function to check registration message and duplicate clients
def checkRegistration(checkMessage, receiveSocket):
    # The split command is put into a try and exceptions are caught
    try:
        (reg, client, chat) = checkMessage.split(" ")
    except ValueError:
        # Print and send 400 Invalid registration
        print("400 Invalid registration")
        receiveSocket.send("400 Invalid registration".encode())

    # Valid message that can be compared with the received message
    validMessage = "REGISTER " + client + " CHAT/1.0"
    # Check format of registration message and presence of username in list
    if checkMessage == validMessage:
        # Checks if client is already registered
        if client not in clientList.values():
            # Include the socket in the socket list
            socketList.append(receiveSocket)
            # Include the client in the dictionary
            clientList[receiveSocket] = client
            # Send the success message
            receiveSocket.send("200 Registration successful".encode())
            # Print the accepted connection details
            print("Accepted connection from client address: " + receiveSocket.recv(1024).decode())
            print("Connection to client established, waiting to receive messages from user '" + client + "'")
        # Client already exists, send error message
        else:
            # Print to server and send to attempting connection that the client name exists
            print("401 Client already registered")
            # Should this be done like this or through std.
            receiveSocket.send("401 Client already registered".encode())
    # Error with message format
    else:
        print("400 Invalid registration")
        receiveSocket.send("400 Invalid registration".encode())
    return client


# Function receiveMessage receives a message at the provided socket
def receiveMessage(receiveSocket, newClient):
    # Tries to receive the message
    try:
        message = receiveSocket.recv(1024).decode()
        # If it's a new connection, newClient will be true and it will check registration
        if newClient:
            checkRegistration(message, receiveSocket)
        # Otherwise check if the message is a disconnect request
        else:
            user = clientList[receiveSocket]
            # Call checkDisconnect function
            if checkDisconnect(message, user):
                print("Disconnecting user " + user)
                # Remove the receiveSocket (key) and the client (item) from the dictionary
                clientList.pop(receiveSocket)
                print(clientList)
                # Remove the socket from the socket list
                socketList.remove(receiveSocket)
                # IS THIS NEEDED?
                # Check if there are any other clients left
                if not clientList:
                    print("No more clients, closing server. Good bye")
                    signal.pause()
                    clientSocket.close()
                    exit()
            # Print the received message and return it
            else:
                print("Received message from user " + clientList[receiveSocket] + ": " + message)
            return message
    # Catches socket errors
    except error as e:
        print("Error reading message: " + e)
        pass


# Function checkDisconnect validates the disconnect message
def checkDisconnect(message, user):
    # Check format of disconnect message
    if message == "DISCONNECT " + user + " CHAT/1.0":
        return True
    else:
        return False


# Server Port, and Address
serverPort = randrange(5000, 12000)

# Server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
# Server will listen for connections
serverSocket.listen()
# List of sockets
socketList = [serverSocket]
# Dictionary containing sockets and the clients
clientList = {}

# Print statements indicating that the server is waiting for clients on a particular port
print('Will wait for client connections at port', serverPort)
print('Waiting for incoming client connections ...')

# clientSocket, addr = serverSocket.accept()

# Receives registration message from client
# regMsg = clientSocket.recv(1024).decode()
# clientUsername = checkRegistration(regMsg)

while True:
    # Checks for user interrupt --> ^C
    signal.signal(signal.SIGINT, signalHandler)

    # Calls select
    readSockets, _, exceptionSockets = select.select(socketList, [], socketList)

    # Loop through notified sockets
    for notifiedSocket in readSockets:
        # New connection since notified socket is server socket
        if notifiedSocket == serverSocket:
            # Accept the new connection
            clientSocket, clientAddress = serverSocket.accept()
            # Call receiveMessage function and pass boolean true that signifies it's a new connection
            clientMessage = receiveMessage(clientSocket, True)
        # It is a pre-existing connection
        else:
            # Call receiveMessage function and pass boolean false that signifies it's not a new connection
            clientMessage = receiveMessage(notifiedSocket, False)
            # Broadcast message to clients other than sender
            for clientSocket in clientList:
                if clientSocket != notifiedSocket:
                    clientSocket.send(clientMessage.encode())
