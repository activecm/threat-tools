<h1 align="center">threat-tools</h1>

This repository contains several scripts that will allow you to mimic a compromised system calling home to a command and control (C2) server. None of the tools exfiltrate any data and are designed to test your environment's ability to detect a wide range of C2 channels.

## Table of Contents
[Overview](#overview)</br>
[Dependencies](#dependencies)</br>
[`simple-listener.sh`](#simple-listenersh)</br>
[`beacon-simulator.py`](#beacon-simulatorpy)</br>
[`beacon-simulator.sh`](#beacon-simulatorsh)</br>
[`simple-beacon.sh`](#simple-beaconsh)</br>
[Python Script Pairs](#python-script-pairs)</br>
[Running Tools in the Background with `screen`](#running-tools-in-the-background-with-screen)


## Overview
In order to run these scripts, you will need two systems: one to act as the compromised client sending the beacon, and one to act as the C2 server. The client will need to run one of the beacon simulator scripts, and the server will need to run one of the scripts to set up a listener. With exception to the scripts within `python-scripts`, all beacon simulators are meant to be used in tandem with `simple-listener.sh` running on the server. The only exception to this is if the client is running `simple-beacon.sh`, which can be used on its own without additional scripts running on the server.

For the majority of users, `beacon-simulator.py` and `simple-listener.sh` will be sufficient to simulate a C2 channel. Alternative beacon simulators are available in the `shell-scripts` and `python-scripts` directories.

## Dependencies
In order to use the tools, you must have `ncat`, `hping3`, and `python3` installed on each of your systems. You will also need to install and use `pip3` to install `pycryptodome` if your system doesn't have it already.

</br>
</br>

## `simple-listener.sh`
`simple-listener.sh` should run on the machine simulating the C2 server. It will set up a listening port for either TCP or UDP connections.

It should be used in conjunction with `beacon-simulator.py`, `beacon-simulator.sh`, or `simple-beacon.sh` running on the machine simulating the compromised client.

### Command Syntax:
```
./simple-listener.sh <port> <protocol>
```
`port`: The port number you want to set up as the listener. Must be root user to listen on ports <= 1024.</br>
`protocol` (optional): The protocol to listen for. Accepts either `udp` or `tcp`. Defaults to `tcp`.

### Example Commands:
```
./simple-listener.sh 9000 udp
```
Sets up port 9000 to listen for UDP connections.

```
./simple-listener.sh 3333
```
Sets up port 3333 to listen for TCP connections.

</br>
</br>

## `beacon-simulator.py`
`beacon-simulator.py` should run on the machine simulating the compromised client. It will allow you to send a jittered beacon with a payload of random size to the targeted IP. The IP should point to the machine acting as the C2 server running `./simple-listener.sh`.

#### Command Syntax
```
python3 ./beacon-simulator.py <ip> <port> <interval> <jitter> <max payload> <protocol>
```
`ip`: The IP address of the server.</br>
`port`: The server port listening for the connection.</br>
`interval`: The amount of time in seconds between beacons.</br>
`jitter`: The amount of jitter in seconds.</br>
`max payload`: The beacon's maximum payload size in bytes. The payload is a random string of a's ranging from 0 to the maximum payload size.</br>
`protocol` (optional): The protocol of the beacon. Accepts either `--tcp` or `--udp`. The TCP protocol is used by default.</br>

#### Example Commands
```
python3 ./beacon-simulator.py -ip 192.168.56.104 -p 9000 -i 30 -j 5 -m 1024
```
Sends a random payload of up to 1024 bytes to port 9000 on the device at IP 192.168.56.104 every 25-35 seconds using the TCP protocol.
```
python3 ./beacon-simulator.py -ip 192.168.56.101 --port 3333 --interval 300 --jitter 8 --max_payload 256 --udp
```
Sends a random payload of up to 256 bytes to port 3333 on the device at IP 192.168.56.101 every 292-308 seconds using the UDP protocol.

</br>
</br>

## `beacon-simulator.sh`
`beacon-simulator.sh` should run on the machine simulating the compromised client. It will allow you to send a jittered beacon with a payload of random size to the targeted IP. The IP should point to the machine acting as the C2 server running `./simple-listener.sh`.

#### Command Syntax
```
./beacon-simulator.sh <ip> <port> <interval> <jitter> <protocol> <max payload>
```
`ip`: The IP address of the server.</br>
`port`: The server port listening for the connection. (Or the ICMP type: 8 = `ping`, 13 = `timestampreq`, 17 = `addrmaskreq`)</br>
`interval`: The amount of time in seconds between beacons.</br>
`jitter`: The amount of jitter in seconds.</br>
`protocol` (optional): The protocol of the beacon. Accepts `tcp`, `udp`, or `icmp`. Defaults to `tcp`.</br>
`max payload` (optional): The beacon's maximum payload size in bytes. The payload is a random string of a's ranging from 0 to the maximum payload size. Defaults to `1424`.</br>

#### Example Commands
```
./beacon-simulator.sh 192.168.56.104 9000 30 5
```
Sends a random payload of up to 1424 bytes to port 9000 on the device at IP 192.168.56.104 every 25-35 seconds using the TCP protocol.

```
./beacon-simulator.sh 192.168.56.101 3333 300 8 udp 256
```
Sends a random payload of up to 256 bytes to port 3333 on the device at IP 192.168.56.101 every 292-308 seconds using the UDP protocol.

```
./beacon-simulator.sh 192.168.56.102 8 10 2 icmp
```
Pings the server at 192.168.56.102 every 8-12 seconds.

</br>
</br>

## `simple-beacon.sh`
`simple-beacon.sh` should run on the machine simulating the compromised client. It sends a very simple HTTP request with a custom user-agent string (`Modzilla/0.0001(Atari7800)`) to a specified IP address or FQDN every 200-350 seconds. It can be used on its own or with `simple-listener.sh` running on the server if you specify a port other than the default `80`.

#### Command Syntax
```
./simple-beacon.sh <IP or FQDN>
```
`IP or FQDN`: The IP address or FQDN of the server.

#### Example Commands
```
./simple-beacon.sh 192.168.56.101
```
Sets up a jittered beacon to port 80 on the server at 192.168.56.101

#### Example Commands
```
./simple-beacon.sh example.com:9000
```
Sets up a jittered beacon to port 9000 on the server at example.com

</br>
</br>

## Python Script Pairs
The scripts within the `python-scripts` directory work in pairs. `tcp-client.py` works with `tcp-server.py`, and `udp-client.py` works with `udp-server.py`. Unlike the other threat tools, these scripts can send a beacon to more than one server. Both client scripts will require editing the code so the IP addresses match your server IP(s). You can also edit the code to configure the server port for the C2 channel, the payload size, and the beaconing interval if you disagree with the defaults.

Default Server Port: 9000</br>
Default Payload Size: 0 - 1200 bytes</br>
Default Beaconing Interval: 30 - 60 seconds

### Configurations
#### Configuring the Client Files
1. On the client device, open `tcp-client.py` or `udp-client.py` in a text editor such as nano.
1. Navigate to the line starting with `server =` followed by a list of IP addresses and replace them with the IP Address(es) of your server(s).
1. (optional) Change the server port at the line with `SERVER_PORT = 9000`. (If you change the port number, you *must* edit the corresponding `-server.py` file to match.)
1. (optional) Change the payload size range at the line with `m = randint(0, 1200)`.
1. (optional) Change the beaconing interval at the line with `rsleep = random.randint(30, 60)`.
1. Save the changes and exit.

#### Configuring Server Files (optional)
NOTE: This is only necessary if you changed the server port number in a `-client.py` script. For example, if you changed the server port in `tcp-client.py`, you *must* edit `tcp-server.py` script to match.
1. On the server device, open the corresponding `-server.py` file in a text editor such as nano.
1. Change the server port number at the line with `SERVER_PORT = 9000` to match the number you chose in the corresponding `-client.py` file.
1. Save the changes and exit.

### Running the Script Pairs
#### TCP Beacon Pair
On the client machine, navigate into the `python-scripts` directory and run:
```
python3 ./tcp-client.py
```
On the server machine, navigate into the `python-scripts` directory and run:
```
python3 ./tcp-server.py
```

#### UDP Beacon Pair
On the client machine, navigate into the `python-scripts` directory and run:
```
python3 ./udp-client.py
```
On the server machine, navigate into the `python-scripts` directory and run:
```
python3 ./udp-server.py
```

</br>
</br>

## Running Tools in the Background with `screen`
You can use the `screen` utility to run these scripts in a separate session in the background and access it later. To do so, simply add `screen -S <name> -d -m` at the beginning of the command, replacing `<name>` with a name for the session.

#### Start session in the background:
```
screen -S my-session -d -m ./simple-beacon.sh 192.168.56.104
```
This will run `simple-beacon.sh` in the background.

If you wish to access the session later and turn it off, you can do so by using `screen -r <name>` to re-attach the session to the terminal window then pressing "Ctrl + C".

#### Re-attaching the session:
```
screen -r my-session
```
This will re-attach `my-session` to the terminal window. I can then stop `simple-beacon.sh` by pressing "Ctrl + C".