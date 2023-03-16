# threat-tools
Tools for simulating threats

beacon-simulator permits you to mimic a compromised system calling home to a command and control (C2) server. This tool will not exfiltrate any data, but is designed to test an environment's ability to detect a wide range of C2 channels. It should be pointed at an Internet IP address that you control (like a cloud instance). <br/> <br/> 
Some command examples: <br/> <br/>
  ./beacon-simulator.sh 192.168.0.1 443 150 12 <br/>
  ./beacon-simulator.sh 192.168.0.7 53 200 10 udp <br/> <br/>
Run the script without switches to access the online help. <br/>
Note: the standard netcat/nc tools included with Linux do not always handle timeouts well, expecially with UDP.  Please install ncat (commonly found in a package called "ncat", or if not, as part of the "nmap" package).  beacon-simulator will prefer to use this if it's installed. <br/> <br/>

python3 ./beacon_simulator.py -ip 192.168.0.5 -p 2000 -i 10 -j 3 -m 1024 <br/>
python3 ./beacon_simulator.py -ip 192.168.0.5 -p 2000 --interval 120 --jitter 12 --max_payload 1024 --tcp <br/>
On your client device: python3 ./tcp_client.py <br/>
On your mock C2 server device: python3 ./tcp_server.py <br/>

For using the client/server python scripts they work in pairs. The UDP
Client script works with the UDP Server script and the TCP Client script
works with the TCP Server script. The client/server scripts require some
manual configuration within the scripts. You will have to put the
destination IP(s) at “server = [your.server.goes.here]”. The port that
the scripts are running on by default is 9000 but it can be changed at
the line with “PORT = 9000” or “SERVER_PORT = 9000”. This script should
scale to as many destinations as you would like to have. Each script has
a printout of each message that is sent, received, and counts the number
of beacons that have currently been sent out. By default the number of
bytes sent for each beacon is a random number between 0 and 1200. This
can be changed at the line with “m = random.randint(0,1200)”. By default
the beaconing interval is between 30 and 60 seconds. This can be changed
at the line with “rsleep = random.randint(30,60)”. The client/server
scripts have a comment on most of the lines with a brief description of
its purpose if you are unsure of it.
