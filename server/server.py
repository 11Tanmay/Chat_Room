# -*- coding: utf-8 -*-
"""Copy of server.ipynb


Now let’s start by implementing the server side first. For this we will need to import two libraries, 
namely socket and threading. The first one will be used for the network connection and the second one 
is necessary for performing various tasks or specifically to run various functions on different threads.
"""

import socket

import threading

"""The next task is to define our connection data and to initialize our socket. We will need an IP address 
and a free port number for our server. In this example, we will use the localhost address (127.0.0.1) and the 
port 5552. The port is actually irrelevant but you have to make sure that the port you are using is free and 
not reserved. If you are running this script on an actual server, specify the IP-address of the server as the host. 
Check out the list of reserved port numbers for more information."""

# Connection Data
host = '127.0.0.1'
port = 5552

# Starting Server / creating a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

"""When we define our socket, we need to pass two arguments. These define the type of socket we want to use. 
The first one (AF_INET) indicates that we are using an internet socket rather than an unix socket. The second
parameter stands for the protocol we want to use. SOCK_STREAM indicates that we are using TCP and not UDP.

After defining the socket, we bind it to our host and the specified port by passing a tuple that contains 
both values. We then put our server into listening mode, so that it waits for clients to connect. At the end we 
create two empty lists, which we will use to store the connected clients and their nicknames later on.
"""

# Sending Messages To All Connected Clients
def broadcast(message):

    for client in clients:
      
        client.send(message)

"""Here we define a little function that is going to help us broadcasting messages and makes the code more 
readable. What it does is just sending a message to each client that is connected and therefore in the clients list.
 We will use this method in the other methods.

Now we will start with the implementation of the first major function. This function will be responsible for 
handling messages from the clients.
"""

# Handling Messages From Clients
def handle(client):

    while True:

        try:

            # Broadcasting Messages
            message = client.recv(1024)

            #If user is to be kicked call kickuser mehod
            if msg.decode('ascii').startswith('KICK'):
              if names[clients.index(client)] == 'admin':
                kickname = msg.decode('ascii')[5:]
                kickuser(kickname)
              else:
                client.send("Command refused!".encode('ascii'))
            # If user is to be banned call kickuser method along with adding to banned list
            elif msg.decode('ascii').startswith('BAN'):
              if names[clients.index(client)] == 'admin':
                banname = msg.decode('ascii')[4:]
                kickuser(banname)
                with open('banned.txt','a') as f:
                  f.write(f'{banname}\n')
                print(f'{banname} was banned!')
              else:
                client.send("Command refused!".encode('ascii'))
            # If it is normal message broadcast it
            else:
              broadcast(message)
        except:
            if client in clients:
            # Removing And Closing Clients
              index = clients.index(client)
              clients.remove(client)
              client.close()
              name = names[index]
              broadcast(f'{name} left the chat\n'.encode('ascii'))
              names.remove(name)
              break

"""As you can see, this function is running in a while-loop. It won’t stop unless there is an exception 
because of something that went wrong. The function accepts a client as a parameter. Everytime a client 
connects to our server we run this function for it and it starts an endless loop.

What it then does is receiving the message from the client (if he sends any) and broadcasting it to all 
connected clients. So when one client sends a message, everyone else can see this message. Now if for 
some reason there is an error with the connection to this client, we remove it and its nickname, close the 
connection and broadcast that this client has left the chat. After that we break the loop and this thread comes to an end.
"""

#Integrating the above methods

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"A client connected with {str(address)}\n")

        # Request And Store Nickname and load banned list
        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        with open('banned.txt','r') as f:
          bans = f.readlines()

        #Login for admin
        if name+'\n' in bans:
          client.send('BAN'.encode('ascii'))
          client.close()
          continue

        if name == 'admin':
          client.send('PASS'.encode('ascii'))
          password = client.recv(1024).decode('ascii')

          if password != 'adminpass':
            client.send('ACCESS DENIED'.encode('ascii'))
            client.close()
            continue

        names.append(name)
		    clients.append(client)
  
        # Print And Broadcast Nickname
        print(f'Name of the client is {name}\n')
        broadcast(f'{name} joined the chat\n'.encode('ascii'))
        client.send("Connected to the server ! Time to chat\n".encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

"""When we are ready to run our server, we will execute this receive function. It also starts an endless 
  while-loop which constantly accepts new connections from clients. Once a client is connected it sends the 
  string ‘NAME’ to it, which will tell the client that its nickname is requested. After that it waits for a 
  response (which hopefully contains the nickname) and appends the client with the respective nickname to the 
  lists. After that, we print and broadcast this information. Finally, we start a new thread that runs the 
  previously implemented handling function for this particular client. Now we can just run this function and our server is done.

  Notice that we are always encoding and decoding the messages here. The reason for this is that we can 
  only send bytes and not strings. So we always need to encode messages (for example using ASCII), when 
  we send them and decode them, when we receive them.
"""

def kickuser(kickname):
  #Kick user from the server
	if kickname in names:
		idx = names.index(kickname)
		kickclient = clients[idx]
		clients.remove(kickclient)
		kickclient.send("You were kicked by an admin!".encode('ascii'))
		kickclient.close()
		names.remove(kickname)
		broadcast(f'{kickname} was kicked by an admin!'.encode('ascii'))

print("Server is listening...")

receive()
