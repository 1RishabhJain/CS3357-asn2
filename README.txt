"""
CS3357 Assignment #2
Oct 19, 2021
Rishabh Jain

README.txt
"""

Welcome to my client-server chat application.

Running this program is simple and is outlined in the steps below:

1. Ensure you have the latest version of python3 installed on your system

2. Open the terminal or command prompt and navigate to the directory where the two files (server.py and client.py) are stored

3. Start the chat server (this must be started first so that clients have something to connect to)

	python3 server.py

4. A line will be printed to the terminal ending with a number. This is the port number that will be used to connect the clients to the server.

5. Start the client. In a new terminal or command prompt window type the following command to connect a client to the server. 

	python3 client.py USERNAME chat://HOSTNAME:PORT	

		Replace USERNAME, with the client name (must be alphabetic)
		Replace HOSTNAME, with the hostname the server is executing on (ex. localhost)
		Replace PORT, with the number noted from step 4.
	
	
	Step 5 can be repeated to connect more clients.

6. The client(s) and server are now connected and can send messages

7. If a particular client wants to disconnect the chat, press CTRL and C on that client's window.

8. To shutdown the server and disconnect all clients, press CTRL and C on the server window.


Enjoy!

