# threat-tools
Tools for simulating threats

beacon-simulator permits you to mimic a compromised system calling home to a command and control server. This tool will not exfiltrate any data, but is designed to test an environment's ability to emulate a wide range of C2 channels. It should be pointed at an Internet IP address that you control (like a cloud instance). The syntax is:
./beacon-simulator <IP> <port> <beacon interval in seconds> <jitter range in seconds>
  ./beacon-simulator.sh 192.168.0.1 443 150 12
  ./beacon-simulator.sh 192.168.0.7 53 200 10 udp
