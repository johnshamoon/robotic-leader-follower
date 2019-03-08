from follower import Follower
from leader import Leader
from tagrec import TagRecognition
import subprocess

"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.
"""

# This function calls the ./bt_toggle script with the specified command and address
def btToggle(command, address):
    subprocess.call(['./bt_toggle.sh',command,address])


def main():
    tag = TagRecognition()
    btAddress = 'EC:83:50:E8:55:67'

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

# This loop makes vehicle move and if the vehicle is a leader and sees an ARTag it will become
# a follower and disconnect from the bluetooth controller

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
