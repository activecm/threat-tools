#Framework of this script can be found here https://github.com/awilk54/Cyber550-Assignment-2
#Written by Mason Bryan mason.bryan@omegaatc.com

import socket
import random
import string
try:
	try:
		from Cryptodome.Cipher import AES #windows
	except:
		from Crypto.Cipher import AES #linux
except:
	print("Missing pycryptodome module. Please run 'pip3 install pycryptodome'")

SERVER_IP = "" #Sets ip as the device current ip address
SERVER_PORT = 9000 #Server Port
CIPHER_KEY=b'bQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r' #Shared Key 32 bytes for 256-bit encryption
TCP_BUFFER= 1024 #Buffer for receiving data
NONCE=b'dRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t' #shared nonce key for validation. 

while True:
	TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize TCP stream
	TCPserver.bind((SERVER_IP, SERVER_PORT)) #Bind TCP Stream connection
	TCPserver.listen(1) #Listen for two TCP connections
	conn, addr = TCPserver.accept() #connection 1 which is client

	while True:
		m = random.randint(5,20) #creates simulated command length
		message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(m)) #creates simulated command
		r1 = random.randint(30,50) #sets one side of the buffer length
		r2 = random.randint(70,90) #sets the other side of the buffer length
		message = ')(' + message + ')(' #creates a way to easily pull out the simulated command
		message = message.rjust(r1,'A') #applies one side of padding buffer
		message = message.ljust(r2,'B') #applies one side of padding buffer
		message = bytes(message, 'utf-8') #converts simulated command to utf-8
		data=conn.recv(TCP_BUFFER) #Client sending cipher message to server
		ciphertext=data
		cipher = AES.new(CIPHER_KEY, AES.MODE_EAX,NONCE) #AES encryption using EAX mode -Encrypt/authenticate/translate
		plaintext = cipher.decrypt(ciphertext) #decryption of cipher message passed from client
		print('Message recieved: ',plaintext) #displays recieved output from client
		print('Message sent: ',message) #displays message to be sent back to client
		CIPHER = AES.new(CIPHER_KEY, AES.MODE_EAX, NONCE) #AES encryption using EAX mode with predefined cipher key and nonce key for validation
		ciphertext, tag = CIPHER.encrypt_and_digest(message) #encrypting message to send to client
		conn.sendall(ciphertext) #send ciphertext of raw message
		print()
		break