"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
from random import *
from socket import *
import signal


def signalHandler(sig, frame):
    print("Interrupt received, shutting down ...")
    discMsg = "DISCONNECT CHAT/1.0"
    connectionSocket.send(discMsg.encode())
    exit()


def checkRegistration(checkMessage):
    # The split command is put into a try and exceptions are caught
    try:
        (reg, client, chat) = checkMessage.split(" ")
    except ValueError:
        # Print and send 400 Invalid registration
        print("400 Invalid registration")
        connectionSocket.send("400 Invalid registration".encode())
        exit()

    validMessage = "REGISTER " + client + " CHAT/1.0"
    # Check format of registration message and presence of username in list
    if checkMessage == validMessage:
        # Checks if client is already registered
        if client not in clientList:
            clientList.append(client)
            connectionSocket.send("200 Registration successful".encode())
            print("Accepted connection from client address: " + connectionSocket.recv(1024).decode())
            print("Connection to client established, waiting to receive messages from user '" + client + "'")
        # Client already exists, send error message
        else:
            print("401 Client already registered")
            connectionSocket.send("401 Client already registered".encode())
            exit()

    # Error with message format
    else:
        print("400 Invalid registration")
        connectionSocket.send("400 Invalid registration".encode())
        exit()

    return client


def checkDisconnect(message, user):
    # Check format of disconnect message
    if message == "DISCONNECT " + user + " CHAT/1.0":
        return True
    else:
        return False


#socketList = []
clientList = []

# Server Port, and Address
serverPort = randrange(5000, 12000)

# Server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# Print statements indicating that the server is waiting for clients on a particular port
print('Will wait for client connections at port', serverPort)
print('Waiting for incoming client connections ...')

connectionSocket, addr = serverSocket.accept()

# Receives registration message from client
regMsg = connectionSocket.recv(1024).decode()
clientUsername = checkRegistration(regMsg)

while True:
    signal.signal(signal.SIGINT, signalHandler)
    message = connectionSocket.recv(1024).decode()
    print("Received message from user " + clientUsername + ": " + message)
    if checkDisconnect(message, clientUsername):
        print("Disconnecting user " + clientUsername)
        clientList.remove(clientUsername)
        if len(clientList) == 0:
            print("No more clients, good bye")
            signal.pause()
            connectionSocket.close()
            exit()
    else:
        connectionSocket.send(message.encode())
    print(clientList)

