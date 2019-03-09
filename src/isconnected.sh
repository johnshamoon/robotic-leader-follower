#!/bin/bash

# This script checks if a Bluetooth device is connected at a specific address.
# This script can be called in this format:
# 	./bt_check.sh $BTADDR 

address=$1

if echo info $address | sudo bluetoothctl | grep -q 'Connected: yes'; then
	exit 1
else
	exit 0
fi	 
