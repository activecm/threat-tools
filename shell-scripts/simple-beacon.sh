#!/bin/bash

# Copyright 2023, Chris Brenton
# Released under GPL 3.0 License

# Command syntax:
# /path/to/simple-beacon.sh <Target IP or FQDN>

while :
    do
        curl -A 'Modzilla/0.0001 (Atari 7800)' $1 >/dev/null 2>&1
        sleep $(shuf -i200-350 -n1)
    done