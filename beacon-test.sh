# !/bin/bash

# Copyright 2023, Chris Brenton
# Released under GPL 3.0 License

# Sample call:
# Then run this command with screen:
# screen -S c2 -d -m /bin/beacon-test <Target IP or FQDN>



while :
    do
        curl -A 'Modzilla/0.0001 (Atari 7800)' $1 >/dev/null 2>&1
        sleep $(shuf -i200-350 -n1)
    done