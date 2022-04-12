# -*- coding: utf-8 -*-
"""client.ipynb

A server is pretty useless without clients that connect to it. So now we are going to implement our client. 
For this, we will again need to import the same libraries. Notice that this is now a second separate script.
"""

import socket

import threading

import time

from datetime import datetime #used for printing date and time of the message sent

"""The first steps of the client are to choose a nickname and to connect to our server. 
We will need to know the exact address and the port at which our server is running."""

name = input("Choose a name: ")

if name == 'admin':
	password = input("Enter password for admin : ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5552

details = (host,port)

client.connect(details)

#define two methods

"""As you can see, we are using a different function here. Instead of binding the data and listening, 
	we are connecting to an existing server.

Now, a client needs to have two threads that are running at the same time. The first one will constantly 
receive data from the server and the second one will send our own messages to the server. So we will need two functions here. Let’s start with the receiving part.
"""

def receive():
	while True:
		global stop
		try:
			message = client.recv(1024).decode('ascii')

			if(message == "NAME"):
				client.send(name.encode('ascii'))
				next_message = client.recv(1024).decode('ascii')
				
				if next_message == 'PASS':
					client.send(password.encode('ascii'))
					
					if(client.recv(1024).decode('ascii')) == 'ACCESS DENIED':
						print('Connection refused by server! Wrong Password!')
						stop = True
				
				elif next_message == "BAN":
					print('Connection refused! User Banned!')
					client.close()
					stop = True
			
			else:
				print(message)
		
		except:
			print("An error occured")
			client.close()
			break

"""Again we have an endless while-loop here. It constantly tries to receive messages 
	and to print them onto the screen. If the message is ‘NAME’ however, it doesn’t print it 
	but it sends its nickname to the server. In case there is some error, we close the connection 
	and break the loop. Now we just need a function for sending messages and we are almost done."""

def write():

	while 1:
		if stop:
			break
		second = time.time()
		date_time = datetime.fromtimestamp(second)
		message = f'{"["+str(date_time)[:19]+"]"} {name} : {input("")}'

		if message[(len(name)+23):].startswith('/'):
			
			if name == 'admin':
				
				if message[(len(name)+23):].startswith('/kick'):
					client.send(f'KICK {message[(len(name)+29):]}'.encode('ascii'))
				
				elif message[(len(name)+23):].startswith('/ban'):
					client.send(f'BAN {message[(len(name)+28):]}'.encode('ascii'))
			
			else:
				print('Commands can be executed by admin only')
		
		else:
			client.send(message.encode('ascii'))

"""The writing function is quite a short one. It also runs in an endless loop 
	which is always waiting for an input from the user. Once it gets some, it combines it 
	with the name and sends it to the server. That’s it. The last thing we need to do 
	is to start two threads that run these two functions."""

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=  write)
write_thread.start()

"""And now we are done. We have a fully-functioning server and working clients that can 
	connect to it and communicate with each other. """
