"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
from random import *
from socket import *

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
# The split command is put into a try and exceptions are caught
try:
    (reg, clientUsername, chat) = regMsg.split(" ")
except ValueError:
    # Print and send 400 Invalid registration
    print("400 Invalid registration")
    connectionSocket.send("400 Invalid registration".encode())
    exit()

# Check format of registration message and presence of username in list
if reg == "REGISTER" and clientUsername.isalpha() and chat == "CHAT/1.0":
    # Checks if client is already registered
    if clientUsername not in clientList:
        print("Accepted connection from client address: ('")
        connectionSocket.send("200 Registration successful".encode())
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

while True:
    sentence = connectionSocket.recv(1024).decode()
    capsSentence = sentence.upper()
    connectionSocket.send(capsSentence.encode())
connectionSocket.close()
