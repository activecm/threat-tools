# Framework for this script can be found here https://github.com/awilk54/Cyber550-Assignment-2
# Written by Mason Bryan mason.bryan@omegaatc.com
# Released under GPL 3.0 License

import socket
import re

try:
	try:
		from Cryptodome.Cipher import AES # Windows
	except:
		from Crypto.Cipher import AES # Linux
except:
	print('Missing pycryptodome module. Please run `pip3 install pycryptodome`')
import random
import string

UDP_SERVER_IP = '' # Sets IP as the device current IP address
UDP_BUFFER = 2048 # Buffer for receiving data
SERVER_PORT = 9000 # Server Port
CIPHER_KEY = b'dRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t' # Shared Key 32 bytes for 256-bit encryption
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP Socket
UDPSocket.bind((UDP_SERVER_IP, SERVER_PORT)) # Bind the socket to IP/Port

while True:
	m = random.randint(5, 20) # Creates simulated command length
	message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(m)) # Creates simulated command
	r1 = random.randint(30, 50) # Sets one side of the buffer length
	r2 = random.randint(70, 90) # Sets one side of the buffer length
	message = ')(' + message + ')(' # Creates a way to easily pull out the simulated command
	message = message.rjust(r1, 'A') # Applies one side of padding buffer
	message = message.ljust(r2, 'B') # Applies one side of padding buffer
	message = bytes(message, 'utf-8') # Converts simulated command to utf-8
	data, addr = UDPSocket.recvfrom(UDP_BUFFER) # Recieving message from client
	ciphertext = data
	data, addr = UDPSocket.recvfrom(UDP_BUFFER) # Recieving nonce from client
	nonce = data
	cipher = AES.new(CIPHER_KEY, AES.MODE_EAX, nonce = nonce) # AES encryption using EAX mode -Encrypt/authenticate/translate
	plaintext = cipher.decrypt(ciphertext) # Decryption of cipher message passed from client
	CIPHER = AES.new(CIPHER_KEY, AES.MODE_EAX) # AES encryption using EAX mode -Encrypt/authenticate/translate
	nonce = CIPHER.nonce
	ciphertext, tag = CIPHER.encrypt_and_digest(message) # Encrypting message to send to client
	UDPSocket.sendto(ciphertext,addr) # Send ciphertext
	UDPSocket.sendto(nonce,addr) # Send NONCE
	try:
		plaintext = plaintext.decode('utf-8')
		plaintext = plaintext.split(',') # Split payload by comma
		plaintext = plaintext[0]
		plaintext = re.sub('[^A-Za-z0-9]+', '', plaintext)
		print()
		print('Message from client: ', plaintext)
		print('Message to client: ', message)
	except:
		continue