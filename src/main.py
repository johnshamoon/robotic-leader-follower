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
    BT_ADDRESS = '5C:BA:37:26:6D:9A'

    # If an ARTag is detected, the vehicle will disconnect from a bluetooth
    # controller. If an ARTag is not detected, the vehicle will connect to
    # a bluetooth controller.
    if tag.detect():
        bt_toggle('disconnect', BT_ADDRESS)
        time.sleep(1)
    else:
        bt_toggle('connect', BT_ADDRESS)
        time.sleep(1)
    if is_controller_connected():
        vehicle = Leader()
    else:
        vehicle = Follower()

    # This loop makes the vehicle move. If the vehicle sees an ARTag then
    # it is a follower vehicle, otherwise it is a leader vehicle.
    start_time = time.time()
    while True:
        if isinstance(vehicle, Leader):
            vehicle.lead()
            if tag.detect():
                bt_toggle('disconnect', BT_ADDRESS)
                time.sleep(1)
                if not is_controller_connected():
                    vehicle = Follower()
        else:
            vehicle.follow()
            if tag.detect():
                start_time = time.time()
            if (time.time() - start_time) > 5:
                bt_toggle('connect', BT_ADDRESS)
                time.sleep(1)
                if is_controller_connected():
                    vehicle = Leader()
                else:
                    start_time = time.time()


if __name__ == '__main__':
    main()
