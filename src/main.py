from follower import Follower
from leader import Leader
from tagrec import TagRecognition

import subprocess
import os

"""
Determines if a Bluetooth controller is connected. 

Returns true if a device is connected and false if not.
"""
def is_controller_connected():
    return os.path.exists('/dev/input/js0')


"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.
"""

def btToggle(command, address):
    subprocess.call(['./bt_toggle',command,address])


def main():
    tag = TagRecognition()
    btAddress = 

    # If an ARTag is detected, there is a vehicle ahead of this vehicle so it will follow.
    # If an ARTag is not detected, no vehicle is present so this vehicle will be a leader.
    if tag.detect() is not None:
        isLeader = False
        print 'I am a follower'
        vehicle = Follower()
        btToggle('disconnect',btAddress)

    else:
        isLeader = True
        print 'I am a leader'
        vehicle = Leader()
        btToggle('connect',btAddress)

    while True:
        if isLeader:
            vehicle.lead()
            if tag.detect() is not None:
                isLeader = False
                print 'I am a follower'
                vehicle = Follower()
                btToggle('disconnect',btAddress)

        else:
            vehicle.follow()

if __name__ == '__main__':
    main()
