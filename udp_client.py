#Framework of this script can be found here https://github.com/awilk54/Cyber550-Assignment-2
#Written by Mason Bryan mason.bryan@omegaatc.com

import socket
try:
	try:
		from Cryptodome.Cipher import AES #windows
	except:
		from Crypto.Cipher import AES #linux
except:
	print("Missing pycryptodome module. Please run 'pip3 install pycryptodome'")
import random
import time
import string

PORT = 9000
UDP_BUFFER=2048
CIPHER_KEY=b'dRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t'
socket.setdefaulttimeout(3)
count = 0

while True:
	server = ["192.168.1.112", "192.168.1.114", "192.168.1.116"] #enter in the server ip addresses to bounce between here
	print(random.choice(server))
	UDP_SERVER_IP = random.choice(server)
	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP Socket
	m = random.randint(0,1200) #Generates the length of the payload to be sent back to the server
	Message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(m)) #creates the string that is to be sent back to the server
	p = random.randint(0,6) #generates the number to decide what is going to be sent back to the server from a "command" from the server
	# print("number: ", p) #debug: prints out the number
	# print("message size: ",m) #debug: prints out how long the message should be
	if p > 4:
		Message = Message
	else:
		Message = "a"
	while True:
		print("Message sent to server: ", Message) #prints out the message to be sent
		Secret_Message= bytes(Message, 'utf-8') #converts payload to utf-8 for transmission
		CIPHER = AES.new(CIPHER_KEY, AES.MODE_EAX) #AES encryption using EAX mode with predefined cipher key and nonce key for validation
		nonce = CIPHER.nonce
		ciphertext, tag = CIPHER.encrypt_and_digest(Secret_Message) #encrypts the payload
		ClientSocket.sendto(ciphertext,(UDP_SERVER_IP,PORT)) #send ciphertext
		ClientSocket.sendto(nonce,(UDP_SERVER_IP,PORT)) #send nonce
		try: 
			data,addr=ClientSocket.recvfrom(UDP_BUFFER) #recieving message from server
			ciphertext=data
			data,addr=ClientSocket.recvfrom(UDP_BUFFER) #recieving message from server
			nonce=data
			cipher = AES.new(CIPHER_KEY, AES.MODE_EAX, nonce=nonce) #AES encryption using EAX mode with predefined cipher key and nonce key for validation
			plaintext = cipher.decrypt(ciphertext) #decryption of cipher message passed from server
			payload_data=plaintext.decode("utf-8") #decode payload data to string
			payload_data2=payload_data.split(",") #split payload by comma
			TEXT=payload_data2[0]
			print("Server sent the following message:", TEXT)
			break
		except:
			break
	ClientSocket.close() #Closes connection in prep for loop to go through again
	rsleep = random.randint(30,60) #generates the amount of random jitter between 30 and 60 seconds
	# print("Sleep time in seconds: "rsleep) #debug: view how long the sleep will be for
	count = count +1
	print("Number of beacons sent: ",count)
	print()
	time.sleep(rsleep)
