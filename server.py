"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
from random import *
from socket import *
import signal
import select

'''
def signalHandler(sig, frame, receiveSocket):
    print("Interrupt received, shutting down ...")
    discMsg = "DISCONNECT CHAT/1.0"
    receiveSocket.send(discMsg.encode())
    exit()
'''


def checkRegistration(checkMessage, receiveSocket):
    # The split command is put into a try and exceptions are caught
    try:
        (reg, client, chat) = checkMessage.split(" ")
    except ValueError:
        # Print and send 400 Invalid registration
        print("400 Invalid registration")
        receiveSocket.send("400 Invalid registration".encode())
        exit()

    validMessage = "REGISTER " + client + " CHAT/1.0"
    # Check format of registration message and presence of username in list
    if checkMessage == validMessage:
        # Checks if client is already registered
        if client not in clientList.values():
            socketList.append(receiveSocket)
            clientList[receiveSocket] = client
            receiveSocket.send("200 Registration successful".encode())
            print("Accepted connection from client address: " + receiveSocket.recv(1024).decode())
            print("Connection to client established, waiting to receive messages from user '" + client + "'")
        # Client already exists, send error message
        else:
            print("401 Client already registered")
            receiveSocket.send("401 Client already registered".encode())
            exit()

    # Error with message format
    else:
        print("400 Invalid registration")
        receiveSocket.send("400 Invalid registration".encode())
        exit()

    return client


def receiveMessage(receiveSocket, boolean):
    try:
        message = receiveSocket.recv(1024).decode()
        if boolean:
            checkRegistration(message, receiveSocket)
        else:
            print("Received message from user " + clientList[receiveSocket] + ": " + message)
            return message
    except:
        print("Error reading message")
        pass


'''
def checkDisconnect(message, user):
    # Check format of disconnect message
    if message == "DISCONNECT " + user + " CHAT/1.0":
        return True
    else:
        return False
'''

# Server Port, and Address
serverPort = randrange(5000, 12000)

# Server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
# Server will listen for connections
serverSocket.listen()
socketList = [serverSocket]
clientList = {}

# Print statements indicating that the server is waiting for clients on a particular port
print('Will wait for client connections at port', serverPort)
print('Waiting for incoming client connections ...')

# clientSocket, addr = serverSocket.accept()

# Receives registration message from client
# regMsg = clientSocket.recv(1024).decode()
# clientUsername = checkRegistration(regMsg)

while True:
    # Checks for ^C

    # signal.signal(signal.SIGINT, signalHandler)

    readSockets, _, exceptionSockets = select.select(socketList, [], socketList)


    for notifiedSocket in readSockets:

        if notifiedSocket == serverSocket:

            clientSocket, clientAddress = serverSocket.accept()

            # recieve message function is called and passes boolean true that signifies it's a new connection
            clientMessage = receiveMessage(clientSocket, True)

        else:

            clientMessage = receiveMessage(notifiedSocket, False)
            for clientSocket in clientList:
                if clientSocket != notifiedSocket:
                    clientSocket.send(clientMessage.encode())

    '''
    if checkDisconnect(clientMessage, clientUsername):
        print("Disconnecting user " + clientUsername)
        clientList.remove(clientUsername)
        if len(clientList) == 0:
            print("No more clients, good bye")
            signal.pause()
            clientSocket.close()
            exit()
    else:
        clientSocket.send(clientMessage.encode())
    '''
    # print(clientList)
