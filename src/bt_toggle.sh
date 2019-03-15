#!/bin/bash

# This script connects and disconnects a Bluetooth device.
# This script can be called in this format:
#     ./bt_toggle.sh $COMMAND $BTADDR
#
# Author: Zein Youssef

command=$1
address=$2

if [[ $command == "connect" ]] || [[ $command == "disconnect" ]]; then
    echo "$command $address" | sudo bluetoothctl
else
    echo 'Invalid Argument'
fi
