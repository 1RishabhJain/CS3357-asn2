# CS3357-asn2
 
Purpose of the Assignment
The general purpose of this assignment is to explore network programming by building a simplified client-server chat application.  This assignment is designed to give you experience in:

writing networked applications
the socket API in Python
writing software supporting a simple protocol
Assigned
Tuesday, September 28, 2021 (please check the main course website regularly for any updates or revisions)

Due
The assignment is due Tuesday, October 19, 2021 by 11:55pm (midnight-ish) through an electronic submission through the OWL site. If you require assistance, help is available online through OWL.

Late Penalty
Late assignments will be accepted for up to two days after the due date, with weekends counting as a single day; the late penalty is 20% of the available marks per day. Lateness is based on the time the assignment is submitted.

Individual Effort
Your assignment is expected to be an individual effort. Feel free to discuss ideas with others in the class; however, your assignment submission must be your own work. If it is determined that you are guilty of cheating on the assignment, you could receive a grade of zero with a notice of this offence submitted to the Dean of your home faculty for inclusion in your academic record.

What to Hand in
Your assignment submission, as noted above, will be electronically through OWL.  You are to submit all Python files required for your assignment (for both your client and your server).   Be sure to include a README file documenting details of how to run and use your application.  (Keep in mind that if the TA cannot run your assignment, it becomes much harder to assign it a grade.)

Assignment Task
You are required to implement in Python a simple client-server chat program.  We are going to start with just basic messaging in this assignment, and then build upon this in Assignment #3 with the ability to follow users or topics, send files, and more!  For now, we will be layering this on top of TCP sockets for reliability, but we will be circling back to this in Assignment #4 and replacing this with UDP sockets and a custom-built reliability layer.

At a high level, your chat application will function like this:

You start by launching your chat server.  It needs to be first as chat clients will need to connect to it to be able to message one another.  When it starts, it picks a random port to listen for clients on, and then reports this port number so that your clients know where to find it.
When you start a chat client, you provide it the address of the server and a user name for use in the chat system.  On startup, the client will establish a connection with the chat server and register itself with the server.  This way, the server knows the client exists to send messages to it later on.  Multiple clients can be started in this fashion and so the server must support communicating with multiple clients at the same time.
To send a message, a user will type it at a prompt provided by their chat client.  Each message is composed of a single line of text.  When the user hits enter/return on their keyboard, their client will send this message to the chat server, prefixed with "@username: ", where username is a user name provided during registration.
When the chat server receives a message from a chat client, the server will broadcast the received message out to every chat client connected and registered at that time, except for the one that originally sent the message.  In this way, every other chat client will receive this message. 
When a chat client receives a message from the chat server, it will display this message for its user.
When a chat client ultimately wants to shut down, it notifies the chat server so the chat server can remove it from its list of connected clients.  Likewise, when the chat server shuts down, it notifies all connected clients, so they can disconnect and shut themselves down.  (If there is no chat server, there is no point for the chat clients to stick around.)
For example, suppose we have started a chat server and it is listening for clients on port 54307.  Users Alice and Bob then start chat clients to connect to this chat server, and exchange messages with one another, taking turns typing and reading messages that come in from the other party.  Alice has to leave and so disconnects from the chat server.  The chat server is then shut down, disconnecting Bob in the process.  This sequence of events is shown in the screen shots below.

 

Chat Server:

<img width="796" alt="chat_server" src="https://user-images.githubusercontent.com/45084203/137527073-1ca542ad-345d-4806-8e69-1cd0a688a624.png">


Alice's Chat Client:

<img width="751" alt="alice_chat_client" src="https://user-images.githubusercontent.com/45084203/137527082-18394421-e9b5-446e-a4ea-c007d1db0966.png">


Bob's Chat Client:


<img width="751" alt="bob_chat_client" src="https://user-images.githubusercontent.com/45084203/137527093-2f2eed9c-235d-4eeb-9cc2-4083f4d2f0eb.png">

 

Some Particulars
Here are some specific requirements and other important notes for this assignment: 

The chat server will not require any command line options. It will have the system select a port number for it to use and report it to the terminal.
The chat client will require two parameters:  the user name for the chat client to use for its user (a single word) and an address for the chat server to connect to, in the form of chat://host:port where host is the hostname the server is executing on and port is the port number it is listening to for requests.  If an invalid address for the server is given, an appropriate error must be reported to the user and the client terminates.  To assist in processing parameters, you can use the argparse package in your application.  To assist in parsing the server address in URL format, I suggest you look at urlparse from the urllib package.  (You may not use any other parts of the urllib package, however.)
As noted above, your chat client and server must communicate to each other using TCP/IP. Your server needs to support multiple connections at a time, and must be able to accept new connections from clients and messages from existing clients at the same time.  To do this, I highly recommend using the selectors package in Python; you can also use the lower level select package instead if you'd rather.  This will let you work with multiple sockets at the same time quite effectively.
Likewise, your chat clients need to be able to both accept new messages typed by the user and messages sent by other users through the chat server at the same time.  (There is no way to tell which will be happening when ... both could happen at any time.)  To enable this, again the selectors package or the select package in Python should do the trick.
All messages sent by users of the chat client are a single line of text.  When sending a message to the chat server, as noted above, the chat client must add "@username: " to the front of the message, where username is the name of the user as specified on the command line when running your chat client.  All such messages received by the chat server are relayed to every connected chat client except for the originator of the message.  (So, to support this, the server must maintain a registration list for connected clients.)
In addition to the text messages sent from the client to the server, other control messages will need to be sent back and forth, with HTTP-styled request and response formatting.  Note that these messages do not begin with an "@username: " unlike regular text messages.
When the chat client starts, it establishes a TCP connection with the server and registers with it.  This registration message is of the form "REGISTER username CHAT/1.0" where username is the name of the user being registered.  If there is an issue with the registration message itself (it is not properly formatted, etc.) the server responds with a "400 Invalid registration" message.  If the user name given during registration is already in use, the server responds with a "401 Client already registered" message.  On receiving either of these responses the chat client prints an error message and terminates.  If the registration message is fine and registration succeeds, the server responds with a "200 Registration successful" message and the client proceeds with messages.  In such a case, the server adds the given user information to a registration list for messaging.
When the user presses Ctrl-C to interrupt the chat client, the chat client must catch that signal (using a signal handler from the signal package) and tell the server it is shutting down.  It does so by sending a "DISCONNECT username CHAT/1.0" message to the server prior to quitting.  On receiving such a message, the server removes its registration for the user in question and does not send back a response.
When the user presses Ctrl-C to interrupt the chat server, the chat server must likewise catch that signal (again using a signal handler from the signal package) and tell all connected clients it is shutting down.  It does so by sending a "DISCONNECT CHAT/1.0" message to each client prior to terminating.  On receiving such a message, a client will print a notice to the user and shut down automatically.
In the absence of user termination via Ctrl-C, both the chat clients and chat server will run continuously, passing messages back and forth.
You are to provide all of the Python code for this assignment yourself, though you may use the sample TCP socket code presented in class as a starting point.  You are not allowed to use Python functions to execute other programs for you, nor are you allowed to use any libraries that do message handling for you.  (If there is a particular library you would like to use/import, other than those listed above and things like socket, os, or sys, you must check first.  You cannot use things like socketserver, for example.)   All server code files must begin with server, and all client files must begin with client.  All of these files must be submitted with your assignment.  (It is possible to have only a single client.py and a single server.py as well.)

As an important note, marks will be allocated for code style. This includes appropriate use of comments and indentation for readability, plus good naming conventions for variables, constants, and functions. Your code should also be well structured (i.e. not all in the main function). 

Please remember to test your program as well, since marks will obviously be given for correctness!  You should run with multiple clients, send messages back and forth, and try various shut down scenarios, with both clients first and the server first.
