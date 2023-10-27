# Framework for this script can be found here https://github.com/awilk54/Cyber550-Assignment-2
# Written by Mason Bryan mason.bryan@omegaatc.com
# Released under GPL 3.0 License

import socket
import random
import string

try:
	try:
		from Cryptodome.Cipher import AES #windows
	except:
		from Crypto.Cipher import AES #linux
except:
	print('Missing pycryptodome module. Please run `pip3 install pycryptodome`')

TCP_SERVER_IP = '' # Sets IP as the device current IP address
TCP_BUFFER = 1024 # Buffer for receiving data
SERVER_PORT = 9000 # Server Port
CIPHER_KEY = b'bQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r' # Shared Key 32 bytes for 256-bit encryption
NONCE = b'dRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t' # Shared NONCE key for validation. 

while True:
	TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialize TCP stream
	TCPserver.bind((TCP_SERVER_IP, SERVER_PORT)) # Bind TCP Stream connection
	TCPserver.listen(1) # Listen for two TCP connections

	while True:
		conn, addr = TCPserver.accept() # Connection 1 which is client
		m = random.randint(5, 20) # Creates simulated command length
		message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(m)) # Creates simulated command
		r1 = random.randint(30, 50) # Sets one side of the buffer length
		r2 = random.randint(70, 90) # Sets the other side of the buffer length
		message = ')(' + message + ')(' # Creates a way to easily pull out the simulated command
		message = message.rjust(r1, 'A') # Applies one side of padding buffer
		message = message.ljust(r2, 'B') # Applies one side of padding buffer
		message = bytes(message, 'utf-8') # Converts simulated command to utf-8
		data = conn.recv(TCP_BUFFER) # Client sending cipher message to server
		ciphertext = data
		cipher = AES.new(CIPHER_KEY, AES.MODE_EAX, NONCE) # AES encryption using EAX mode -Encrypt/authenticate/translate
		plaintext = cipher.decrypt(ciphertext) # Decryption of cipher message passed from client
		print('Message from client: ', plaintext) # Prints recieved output from client
		print('Message to client: ', message) # Prints message to be sent back to client
		CIPHER = AES.new(CIPHER_KEY, AES.MODE_EAX, NONCE) # AES encryption using EAX mode with predefined cipher key and NONCE key for validation
		ciphertext, tag = CIPHER.encrypt_and_digest(message) # Encrypting message to send to client
		conn.sendall(ciphertext) # Send ciphertext of raw message
		print()
