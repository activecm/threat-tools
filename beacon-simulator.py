# Based off of beacon-simulator.sh written by Bill Stearns bill@activecountermeasures.com
# Written by Mason Bryan mason.bryan@omegaatc.com
# Released under GPL 3.0 License
# Version 1

# The payload is a random number of 'a' 's (between 0 and max_payload_size a's).
# Note: the payload _is never sent_ if using TCP and the remote port is closed.

import socket, time, random, argparse

parser = argparse.ArgumentParser(description="Example command: 'python3 .\\beacon-simulator.py -ip 192.168.0.5 -p 2000 -i 10 -j 3 -m 1024' or 'python3 .\\beacon-simulator.py -ip 192.168.0.5 -p 2000 --interval 120 --jitter 12 --max_payload 1024 --tcp'")
parser.add_argument("-ip", dest="ip", type=str, help="Use -ip in order to set your target IP address.", required=True)
parser.add_argument("-p", "--port", type=int, dest="port", help="Use -p to specifiy a port for use.", required=True)
parser.add_argument("-i", "--interval", type=int, dest="interval", help="Use -i to specify an interval for the beacon in seconds.", required=True)
parser.add_argument("-j", "--jitter", type=int, dest="jitter", help="Use -j to specify the amount of jitter to be used in seconds.", required=True)
parser.add_argument("--tcp", dest="tcp", action="store_true", help="Use -t to select the tcp protocol. This is optional and TCP is default.", required=False)
parser.add_argument("--udp", dest="udp", action="store_true", help="Use -u to select the udp protocol. This is optional and TCP is default.", required=False)
parser.add_argument("-m", "--max_payload", type=int, dest="max_payload", help="Use -m to set a maximum payload size.", required=True)
args = parser.parse_args()

server_ip = args.ip
server_port = args.port
max_size = args.max_payload
data = "a"
interval = args.interval
variance = args.jitter
jitter = random.randint(interval - variance, interval + variance)

def tcp_beacon():
    count = 0
    while True:
        message_size = random.randint(0,max_size)
        message = "".join([data]*message_size)
        message = bytes(message, 'utf-8')
        jitter = random.randint(interval - variance, interval + variance)
        print("amount of jitter: ",jitter)
        print("data sent: ",message)
        client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp.connect((server_ip, server_port))
        client_tcp.sendall(message)
        client_tcp.close()
        count = count +1
        print("Number of beacons sent: ",count)
        time.sleep(jitter)

def udp_beacon():
    count = 0
    while True:
        message_size = random.randint(0,max_size)
        message = "".join([data]*message_size)
        message = bytes(message, 'utf-8')
        jitter = random.randint(interval - variance, interval + variance)
        print("Amount of jitter: ",jitter)
        print("Data sent: ",message)
        client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_udp.sendto(message, (server_ip, server_port))
        client_udp.close()
        count = count +1
        print("Number of beacons sent: ",count)
        time.sleep(jitter)

if args.tcp:
    tcp_beacon()
elif args.udp:
    udp_beacon()
else:
    tcp_beacon()