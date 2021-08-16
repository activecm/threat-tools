#!/bin/bash
#Copyright 2021 Active Countermeasures
#Based on ideas from Chris Brenton
#Written by Bill Stearns bill@activecountermeasures.com
#Released under the GPL
#V0.3

Usage () {
	echo 'Parameters:' >&2
	echo '	1: target ip' >&2
	echo '	2: port' >&2
	echo '	3: interval' >&2
	echo '	4: jitter' >&2
	echo '	5: optional protocol (default is   tcp   ; put   udp  here if you want that)' >&2
	echo '' >&2
	echo 'Examples:' >&2
	echo "$0 192.168.0.1 9999 150 12" >&2
	echo "$0 192.168.0.7 514 200 10 udp" >&2
	exit 1
}

if which ncat >/dev/null ; then
	netcat_bin=`which ncat`
elif which nc >/dev/null ; then
	netcat_bin=`which nc`
elif which netcat >/dev/null ; then
	netcat_bin=`which netcat`
elif [ -n "$BASH_VERSION" ]; then
	netcat_bin=''						#We'll use bash's built-in ability to make TCP connections
else
	echo 'Unable to locate netcat and not running under bash, exiting.' >&2
	exit 1
fi


if [ "z$1" = "z--help" -o "z$1" = "z-h" ]; then
	Usage
elif [ -z "$4" -o -n "$6" ]; then
	echo "Incorrect number of parameters, exiting."
	Usage
fi

if [ "$3" -lt "$4" ]; then
	echo 'Jitter cannot be greater than the interval, exiting.' >&2
	exit 1
fi

if [ "$5" = "udp" ]; then
	proto_flag=' -u '
	proto_acronym='udp'
else
	proto_flag=' '
	proto_acronym='tcp'
fi


echo "Will connect to host $1, $proto_acronym port $2 every $3 +/-(${4}/2) seconds" >&2
while : ; do
	if [ -n "$netcat_bin" ]; then
		if [ "$proto_acronym" = "udp" ]; then
			echo ' ' | "$netcat_bin" $proto_flag "$1" "$2" >/dev/null 2>/dev/null
		else
			"$netcat_bin" $proto_flag -w 10 "$1" "$2" </dev/null >/dev/null 2>/dev/null
		fi
	else
		if [ "$proto_acronym" = "udp" ]; then
			#For some reason the packet is never sent if stdout is redirected to /dev/null
			echo -n ' ' >"/dev/$proto_acronym/$1/$2"
		else
			echo -n ' ' >"/dev/$proto_acronym/$1/$2" >/dev/null 2>/dev/null
		fi
	fi

	echo -n '.'
	naptime=$[ (($RANDOM * $4) / 32767) - ($4 / 2) + $3 ]
	#echo "Sleeping for $naptime"
	sleep "$naptime"
done
