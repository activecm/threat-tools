#!/bin/bash

# Copyright 2022, Active Countermeasures
# Written by Bill Stearns bill@activecountermeasures.com
# Released under GPL 3.0 License
# Version 0.1

# Sets up a simple listening TCP or UDP port suitable for accepting a connections from beacon-simulator.sh


Usage() {
	echo 'Parameters:' >&2
	echo '  Port number to listen on (on all platforms except windows you must be root to listen on ports <=1024)' >&2
	echo '  Protocol (UDP or TCP, default is TCP)' >&2
	exit 1
}


if which ncat >/dev/null ; then
	netcat_bin=`which ncat`
elif which nc >/dev/null ; then
	if [ "$2" = "udp" -o "$2" = "UDP" ]; then
		echo "The 'nc' form of netcat may not correctly handle udp timeouts correctly.  Please install 'ncat'" >&2
	fi
	netcat_bin=`which nc`
elif which netcat >/dev/null ; then
	if [ "$2" = "udp" -o "$2" = "UDP" ]; then
		echo "The 'netcat' form of netcat may not correctly handle udp timeouts correctly.  Please install 'ncat'" >&2
	fi
	netcat_bin=`which netcat`
else
	echo 'Unable to locate netcat, exiting.' >&2
	exit 1
fi


if [ -z "$1" -o -n "$3" ]; then
	Usage
fi

listen_port="$1"
if [ "$2" = "udp" -o "$2" = "UDP" ]; then
	listen_proto='UDP'
	listen_param=' -u -i 3 '
elif [ "$2" = "tcp" -o "$2" = "TCP" -o "$2" = '' ]; then
	listen_proto='TCP'
	listen_param=' -k '
else
	Usage
fi


while : ; do
	echo "Starting listener on $listen_proto port $listen_port" >&2
	$netcat_bin -l $listen_param $listen_port </dev/null >/dev/null 2>&1
done



