"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
from random import *
from socket import *

# Server Name, Server Port, and Address
serverName = 'localhost'
serverPort = 5050
address = ('', serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input: ')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()