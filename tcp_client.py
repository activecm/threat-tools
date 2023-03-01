#Framework of this script can be found here https://github.com/awilk54/Cyber550-Assignment-2
#Written by Mason Bryan mason.bryan@omegaatc.com

import socket
import time
import random
import string
try:
	try:
		from Cryptodome.Cipher import AES #windows
	except:
		from Crypto.Cipher import AES #linux
except:
	print("Missing pycryptodome module. Please run 'pip3 install pycryptodome'")

SERVER_PORT = 9000 # server Port
CIPHER_KEY=b'bQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r' #Shared Encryption/decryption Key
NONCE=b'dRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t' #shared NONCE key for validity
socket.setdefaulttimeout(3)
count = 0

while True:
	server = ["192.168.1.111", "192.168.1.113", "192.168.1.115"] #enter in the server ip addresses to bounce between here
	print(random.choice(server))
	SERVER_IP = random.choice(server)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket creation
	try:
		client.connect((SERVER_IP, SERVER_PORT)) #TCP connection
		m = random.randint(0,1200) #Generates the length of the payload to be sent back to the server
		Message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(m)) #creates the string that is to be sent back to the server
		p = random.randint(0,6) #generates the number to decide what is going to be sent back to the server from a "command" from the server
		print("number: ", p) #debug: prints out the number
		print("message size: ",m) #debug: prints out how long the message should be
		if p > 4:
			Message = Message
		else:
			Message = "a"
		while True:
			Message = bytes(Message, 'utf-8') #converts payload to utf-8 for transmission
			print('Message sent: ',Message) #prints out the message to be sent
			CIPHER = AES.new(CIPHER_KEY, AES.MODE_EAX, NONCE) #AES encryption using EAX mode with predefined cipher key and nonce key for validation
			ciphertext, tag = CIPHER.encrypt_and_digest(Message) #encrypts the payload
			try:
				client.sendall(ciphertext) #send ciphertext of raw message
				try:
					data=client.recv(1024) #Client sending cipher message
					ciphertext=data
					cipher = AES.new(CIPHER_KEY, AES.MODE_EAX,NONCE) #AES encryption using EAX mode -Encrypt/authenticate/translate
					plaintext = cipher.decrypt(ciphertext) #decryption of cipher message passed from client 
					print('Message recieved: ',plaintext) #prints message back from server
					break
				except:
					break
			except:
				break
		client.close() #Closes connection in prep for loop to go through again
	except:
		break
	rsleep = random.randint(30,60) #generates the amount of random jitter between 30 and 60 seconds
	# print("Sleep time in seconds: "rsleep) #debug: view how long the sleep will be for
	count = count +1
	print("Number of beacons sent: ",count)
	print()

	time.sleep(rsleep)
