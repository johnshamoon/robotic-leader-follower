import os

from follower import Follower
from leader import Leader
from tagrec import TagRecognition

"""
Returns whether or not a Bluetooth joystick is connected.
"""
def is_connected():
    return os.path.exists('/dev/input/js0')


"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.
"""
def main():
    tag = TagRecognition()

    # If an ARTag is detected, there is a vehicle ahead of this vehicle so it will follow.
    # If an ARTag is not detected, no vehicle is present so this vehicle will be a leader.
    if tag.detect() is not None:
        follower = Follower()
        while True:
            follower.follow()
    else:
        leader = Leader()
        while True:
            leader.lead()


if __name__ == '__main__':
    main()
