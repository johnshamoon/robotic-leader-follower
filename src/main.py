"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.
"""

from follower import Follower
from leader import Leader
from tagrec import TagRecognition

import os
import subprocess
import time

"""
Determines if a Bluetooth controller is connected. 

Returns true if a device is connected and false if not.
"""
def is_controller_connected():
    return os.path.exists('/dev/input/js0')


"""
This function calls the ./bt_toggle script with the specified
command and address
"""
def bt_toggle(command, address):
    subprocess.call(['./bt_toggle.sh', command, address])


def main():
    tag = TagRecognition()
    bt_address = '5C:BA:37:26:6D:9A'

    # If an ARTag is detected, the vehicle will try to disconnect from a bluetooth controller and
    # if it is not connected to one it will follow. If an ARTag is not detected, the vehicle will
    # will try to connect to the bluetooth controller and if succeful, the vehicle will be a leader.
    if tag.detect():
        bt_toggle('disconnect', bt_address)
    else:
        bt_toggle('connect', bt_address)
    if is_controller_connected():
        vehicle = Leader()
    else:
        vehicle = Follower()

    # This loop makes vehicle move. If the vehicle is a leader and sees an ARTag
    # it will attempt to disconnect from the bluetooth controller, if done
    # successfully it will become a follower vehicle. If the vehicle is a follower
    # and does not see an ARTag for more than 5 seconds, the it will try to connect
    # to the bluetooth controller. If done successfully it will become a leader, otherwise
    # it will continue as a follower and reset the 5 second timer before trying to
    # connect to the bluetooth controller again.
    start_time = time.time()
    while True:
        if isinstance(vehicle, Leader):
            vehicle.lead()
            if tag.detect():
                bt_toggle('disconnect', bt_address)
                if not is_controller_connected():
                    vehicle = Follower()
        else:
            vehicle.follow()
            if tag.detect():
                start_time = time.time()
            if (time.time() - start_time) > 5:
                bt_toggle('connect', bt_address)     
                if is_controller_connected():
                    vehicle = Leader()
                else:
                    start_time = time.time()


if __name__ == '__main__':
    main()
