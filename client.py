"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain
"""
from socket import *
import sys
import argparse
from urllib.parse import urlparse
import signal
import selectors

sel = selectors.DefaultSelector()


# Functions to assist with the program

# Function signalHandler handles user interrupt ^C
def signalHandler(sig, frame):
    print("Interrupt received, shutting down ...")
    discMsg = "DISCONNECT " + clientUsername + " CHAT/1.0"
    clientSocket.send(discMsg.encode())
    sel.unregister(clientSocket)
    signal.pause()
    clientSocket.close()
    exit()


def checkDisconnect(discMessage):
    # Check format of disconnect message
    if discMessage == "DISCONNECT CHAT/1.0":
        sel.unregister(clientSocket)
        signal.pause()
        clientSocket.close()
        quit()
        #return True
    else:
        #return False
        pass


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
        print("Registration successful. Ready for messaging!")
        sel.register(sys.stdin, selectors.EVENT_READ, readStdin)
        sel.register(clientSocket, selectors.EVENT_READ, readServer)

        # Sends client socket information to server
        client.send(str(clientSocket.getsockname()).encode())
        return True


def readStdin(terminal, mask):
    inputMessage = terminal.readline()
    inputMessage = ("@" + clientUsername + " " + inputMessage)
    clientSocket.send(inputMessage.encode())


def readServer(cSocket, mask):
    receivedMessage = cSocket.recv(1024)
    checkDisconnect(receivedMessage)
    print('From Server:', receivedMessage.decode())


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
    exitStatus = signal.signal(signal.SIGINT, signalHandler)
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)

    # message = ("@" + clientUsername + " " + inputMessage)
    # clientSocket.send(message.encode())






# In addition to the text messages sent from the client to the server, other control messages will need to be sent back and forth, with HTTP-styled request and response formatting.  Note that these messages do not begin with an "@username: " unlike regular text messages.