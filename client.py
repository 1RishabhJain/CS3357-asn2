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


def signalHandler(sig, frame):
    print("Interrupt received, shutting down ...")
    discMsg = "DISCONNECT " + clientUsername + " CHAT/1.0"
    clientSocket.send(discMsg.encode())
    exit()


def checkDisconnect():
    # Check format of disconnect message
    if message == "DISCONNECT CHAT/1.0":
        return True
    else:
        return False


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
    clientUsername = args.username
    url = urlparse(args.address)
    hostname = url.hostname
    port = url.port

    # Checking validity of provided arguments
    if clientUsername.isalpha():
        if bool(url.scheme) and bool(url.port):
            pass
        else:
            print("Error with address, please try again")
            exit()
    else:
        print("Error with username, please try again")
        exit()

    # Remainder of program executes if the username, host, and port are valid
    print("Connecting to server ...")

    # Creating socket and connecting
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Checking for connection errors
    try:
        clientSocket.connect((hostname, port))
        print("Connection to server established. Sending intro message ...\n")
    except ConnectionError or ConnectionRefusedError:
        print("Connection unsuccessful, check address details and try again")
        exit()

    # Creating and sending registration message
    regMsg = "REGISTER " + clientUsername + " CHAT/1.0"
    clientSocket.send(regMsg.encode())

    # Receiving registration response from server
    regMsgResponse = clientSocket.recv(1024).decode()

    # Error with registration
    if regMsgResponse == "400 Invalid registration" or regMsgResponse == "401 Client already registered":
        print(regMsgResponse)
        exit()

    # Successful registration
    if regMsgResponse == "200 Registration successful":
        print("Registration successful. Ready for messaging!")

    # Sends client socket information to server
    clientSocket.send(str(clientSocket.getsockname()).encode())

    while True:
        signal.signal(signal.SIGINT, signalHandler)
        #checkDisconnect()
        inputMessage = input('Input: ')
        message = ("@" + clientUsername + " " + inputMessage)
        clientSocket.send(message.encode())
        receivedMessage = clientSocket.recv(1024)
        print('From Server:', receivedMessage.decode())
    signal.pause()
    clientSocket.close()

else:
    print("Error with arguments, please try again")
    exit()
