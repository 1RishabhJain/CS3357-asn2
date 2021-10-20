"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain

client.py
"""

from urllib.parse import urlparse
from socket import *
import sys
import argparse
import signal
import selectors

# Selectors
sel = selectors.DefaultSelector()


# Function signalHandler handles user interrupt ^C
def signalHandler(sig, frame):
    # Print interrupt message
    print("Interrupt received, shutting down ...")
    # Create and send disconnect message
    discMsg = "DISCONNECT " + clientUsername + " CHAT/1.0"
    clientSocket.send(discMsg.encode())
    # Unregister socket, close and exit
    sel.unregister(clientSocket)
    clientSocket.close()
    exit()


# Function to validate the command line arguments provided when client is run
def validateArgs():
    if len(sys.argv) == 3:
        # Using argparse
        parser = argparse.ArgumentParser()
        # The first argument: the user name for the chat client to use for its user
        parser.add_argument("username")
        # The second argument: address for the chat server to connect to
        parser.add_argument("address")
        # Parsing the arguments
        args = parser.parse_args()

        # Storing parsed values into variables
        username = args.username
        url = urlparse(args.address)
        argHostname = url.hostname
        argPort = url.port

        # Checking validity of provided arguments
        if username.isalpha():
            if bool(url.scheme) and bool(url.port):
                return username, argHostname, argPort
            else:
                print("Error with address, please try again")
                exit()
        else:
            print("Error with username, please try again")
            exit()
    else:
        print("Error with arguments, please try again")
        exit()


# Steps required to establish the initial connection to the server
def initialConnection():
    print("Connecting to server ...")

    # Creating socket and connecting
    client = socket(AF_INET, SOCK_STREAM)

    # Checking for connection errors
    try:
        client.connect((hostname, port))
    except ConnectionError or ConnectionRefusedError:
        print("Connection unsuccessful, check address details and try again")
        exit()

    # Successful connection
    print("Connection to server established. Sending intro message ...\n")
    return client


# Registration message function is used to send and validate the registration message
def regMessage(client):
    # Creating and sending registration message
    regMsg = "REGISTER " + clientUsername + " CHAT/1.0"
    client.send(regMsg.encode())

    # Receiving registration response from server
    regMsgResponse = client.recv(1024).decode()

    # Error with registration
    if regMsgResponse == "400 Invalid registration" or regMsgResponse == "401 Client already registered":
        print(regMsgResponse)
        exit()

    # Successful registration
    if regMsgResponse == "200 Registration successful":
        client.send(str(client.getsockname()).encode())
        print("Registration successful. Ready for messaging!")
        sel.register(sys.stdin, selectors.EVENT_READ, readStdin)
        sel.register(clientSocket, selectors.EVENT_READ, readServer)
        return True
    else:
        return False


# Function to read terminal input
def readStdin(terminal, mask):
    # Read line
    inputMessage = terminal.readline()
    # Append '@' symbol and the client's name to the message
    modifiedMessage = ("@" + clientUsername + " " + inputMessage)
    # Send the modified message
    clientSocket.send(modifiedMessage.encode())


# Function to read server events
def readServer(cSocket, mask):
    receivedMessage = cSocket.recv(1024).decode()
    # Check format of disconnect message
    if receivedMessage == "DISCONNECT CHAT/1.0":
        print("Disconnected from server ... exiting!")
        sel.unregister(cSocket)
        cSocket.close()
        quit()
    else:
        print(receivedMessage)


# Boolean to store connected state
connected = False

# Repeats the following functions until a valid connection is established
while not connected:
    # Calls function to validate the arguments, if there is any error then it will exit the program
    clientUsername, hostname, port = validateArgs()

    # Calls initialConnection function to establish the connection
    clientSocket = initialConnection()

    # Calls regMessage function to send and validate the registration message
    connected = regMessage(clientSocket)


while True:
    # Checks for user interrupt --> ^C
    signal.signal(signal.SIGINT, signalHandler)

    # Selectors
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
