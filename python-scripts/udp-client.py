# Framework for this script can be found here https://github.com/awilk54/Cyber550-Assignment-2
# Written by Mason Bryan mason.bryan@omegaatc.com
# Released under GPL 3.0 License

import socket
import random
import time
import string

try:
	try:
		from Cryptodome.Cipher import AES # Windows
	except:
		from Crypto.Cipher import AES # Linux
except:
	print('Missing pycryptodome module. Please run `pip3 install pycryptodome`')

SERVER_PORT = 9000
UDP_BUFFER = 2048
CIPHER_KEY = b'dRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t' # Shared encryption/decryption key
socket.setdefaulttimeout(3)
count = 0

while True:
	server = ['192.168.1.112', '192.168.1.114', '192.168.1.116'] # Enter a single server IP address or multipe server IPs to bounce between
	print(random.choice(server))
	UDP_SERVER_IP = random.choice(server)
	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP Socket
	m = random.randint(0,1200) # Sets a random size for the payload to be sent back to the server
	Message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(m)) # Creates the string to be sent back to the server
	p = random.randint(0,6) # Generates the number to decide what is going to be sent back to the server from a "command" from the server
	# print('number: ', p) # Debug: prints out the number
	# print('message size: ',m) # Debug: prints out how long the message should be
	if p > 4:
		Message = Message
	else:
		Message = 'a'
	while True:
		print('Message sent to server: ', Message) # Prints the message to be sent
		Secret_Message = bytes(Message, 'utf-8') # Converts payload to utf-8 for transmission
		CIPHER = AES.new(CIPHER_KEY, AES.MODE_EAX) # AES encryption using EAX mode with predefined cipher key for validation
		nonce = CIPHER.nonce
		ciphertext, tag = CIPHER.encrypt_and_digest(Secret_Message) # Encrypts the payload
		ClientSocket.sendto(ciphertext,(UDP_SERVER_IP,SERVER_PORT)) # Send ciphertext
		ClientSocket.sendto(nonce,(UDP_SERVER_IP,SERVER_PORT)) # send NONCE
		try: 
			data,addr = ClientSocket.recvfrom(UDP_BUFFER) # Recieving message from server
			ciphertext = data
			data,addr = ClientSocket.recvfrom(UDP_BUFFER) # Recieving message from server
			nonce = data
			cipher = AES.new(CIPHER_KEY, AES.MODE_EAX, nonce = nonce) # AES encryption using EAX mode with predefined cipher key and NONCE key for validation
			plaintext = cipher.decrypt(ciphertext) # Decryption of cipher message passed from server
			payload_data = plaintext.decode('utf-8') # Decode payload data to string
			payload_data2 = payload_data.split(',') # Split payload by comma
			TEXT = payload_data2[0]
			print('Server sent the following message:', TEXT)
			break
		except:
			break
	ClientSocket.close() # Closes connection in preparation for next loop iteration
	rsleep = random.randint(30,60) # Generates the amount of random jitter between 30 and 60 seconds
	# print('Sleep time in seconds: 'rsleep) # Debug: View how long the sleep will be
	count = count + 1
	print('Number of beacons sent: ', count)
	print()
	time.sleep(rsleep)
