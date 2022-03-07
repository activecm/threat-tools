#!/bin/bash
#Copyright 2021 Active Countermeasures
#Based on ideas from Chris Brenton
#Written by Bill Stearns bill@activecountermeasures.com
#Released under the GPL
#V0.6
#The payload is a random number of 'a' 's (between 0 and 1424 a's).
#Note: the payload _is not sent_ if using TCP and the remote port is closed.

Usage () {
	echo 'Parameters:' >&2
	echo '	1: target ip' >&2
	echo '	2: port' >&2
	echo '	3: interval' >&2
	echo '	4: jitter (max deviation from interval)' >&2
	echo '	5: optional protocol (default is   tcp   ; put   udp   here if you want that)' >&2
	echo '      (you must specify tcp or udp if you want to force max_payload_size)' >&2
	echo '	6: max_payload_size (a payload with a random number of characters between 0 bytes and this value will be sent)' >&2
	echo '' >&2
	echo 'Examples:' >&2
	echo "$0 192.168.0.1 9999 150 12" >&2
	echo "$0 192.168.0.7 514 200 10 udp" >&2
	echo "$0 192.168.0.7 9999 150 12 tcp 1000" >&2
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
elif [ -z "$4" -o -n "$7" ]; then
	echo "Incorrect number of parameters, exiting."
	Usage
fi

if [ "$3" -lt "$4" ]; then
	echo 'Jitter cannot be greater than the interval, exiting.' >&2
	exit 1
fi

if [ "$5" = "udp" -o "$5" = "UDP" ]; then
	proto_flag=' -u '
	proto_acronym='udp'
else
	proto_flag=' '
	proto_acronym='tcp'
fi

if [ -n "$6" ]; then
	if [[ $6 =~ ^0+$ ]]; then
		max_payload_size="none"
		random_divisor="1"		#Won't be used
	elif [[ $6 =~ ^[[:digit:]]+$ ]]; then
		max_payload_size="$6"
		random_divisor=$((32767 / $max_payload_size))
	else
		echo "max_payload_size field contains non-digits: $6 .  Exiting." >&2
		exit 1
	fi
else
	max_payload_size="1424"
	random_divisor="23"
fi

echo "Will connect to host $1, $proto_acronym port $2 every $3 +/-(${4}) seconds, max payload of $max_payload_size bytes." >&2
while : ; do
	if [ "$max_payload_size" = "none" ]; then
		random_payload=''
	else
		random_payload=`dd if=/dev/zero bs=1 count=$[ $RANDOM / $random_divisor ] 2>/dev/null | tr '\0' 'a'`		#Creates between 0 and max_payload_size letter a's as a payload
	fi

	if [ -n "$netcat_bin" ]; then
		if [ "$proto_acronym" = "udp" ]; then
			echo -n "$random_payload" | "$netcat_bin" $proto_flag "$1" "$2" >/dev/null 2>/dev/null
		else
			echo -n "$random_payload" | "$netcat_bin" $proto_flag -w 10 "$1" "$2" >/dev/null 2>/dev/null
		fi
	else
		if [ "$proto_acronym" = "udp" ]; then
			#For some reason the packet is never sent if stdout is redirected to /dev/null
			echo -n "$random_payload" >"/dev/$proto_acronym/$1/$2"
		else
			echo -n "$random_payload" >"/dev/$proto_acronym/$1/$2" 2>/dev/null
		fi
	fi

	echo -n '.'
	naptime=$[ (($RANDOM * $4 * 2) / 32767) - ($4) + $3 ]	#"random value between 0 and 1 * 2x jitter", minus 1x jitter plus interval
	#echo "Sleeping for $naptime"
	sleep "$naptime"
done
