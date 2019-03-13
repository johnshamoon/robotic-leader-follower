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

import subprocess
import time

"""
This function calls the ./bt_toggle script with the specified
command and address
"""
def bt_toggle(command, address):
    subprocess.call(['./bt_toggle.sh', command, address])


def main():
    tag = TagRecognition()
    bt_address = '5C:BA:37:26:6D:9A'

    # If an ARTag is detected, there is a vehicle ahead of this vehicle so it will follow.
    # If an ARTag is not detected, no vehicle is present so this vehicle will be a leader.
    if tag.detect():
        bt_toggle('disconnect', bt_address)
        is_leader = False
        vehicle = Follower()
    else:
        bt_toggle('connect', bt_address)
        is_leader = True
        vehicle = Leader()

    # This loop makes vehicle move and if the vehicle is a leader and sees an ARTag
    # it will become a follower and disconnect from the bluetooth controller
    while True:
        if is_leader:
            vehicle.lead()
            if tag.detect():
                bt_toggle('disconnect', bt_address)
                is_leader = False
                vehicle = Follower()
        else:
            vehicle.follow()
            if tag.detect():
                start_time = time.time()
            if (time.time() - start_time) > 5:
                bt_toggle('connect', bt_address)     
                is_leader = True
                vehicle = Leader()


if __name__ == '__main__':
    main()
