# threat-tools
Tools for simulating threats

beacon-simulator permits you to mimic a compromised system calling home to a command and control (C2) server. This tool will not exfiltrate any data, but is designed to test an environment's ability to detect a wide range of C2 channels. It should be pointed at an Internet IP address that you control (like a cloud instance). <br/> <br/> 
Some command examples: <br/> <br/>
  ./beacon-simulator.sh 192.168.0.1 443 150 12 <br/>
  ./beacon-simulator.sh 192.168.0.7 53 200 10 udp <br/> <br/>
Run the script without switches to access the online help. <br/>
