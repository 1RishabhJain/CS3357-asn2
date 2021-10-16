"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
from random import *
from socket import *

# Server Port, and Address
#serverPort = randrange(5000, 12000)
serverPort = 5050
address = ('', serverPort)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(address)

serverSocket.listen(1)

# Print statements indicating that the server is waiting for clients on a particular port
print('Will wait for client connections at port', serverPort)
print('Waiting for incoming client connections ...')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capsSentence = sentence.upper()
    connectionSocket.send(capsSentence.encode())
    connectionSocket.close()