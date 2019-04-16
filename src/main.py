"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.

Authors: Zein Youssef and Steven Dropiewski
"""
from follower import Follower
from leader import Leader
from tagrec import TagRecognition


def decide_role(tag_data):
    """
    Creates a Leader or Follower object.

    :param tag_data: Return value of TagRecognition.detect().

    :return: If tag_data is None, the vehicle will become a Leader. Otherwise,
             it will become a Follower.
    :rtype: Leader or Follower
    """
    if tag_data:
        vehicle = Follower()
    else:
        vehicle = Leader()

    return vehicle


def main():
    """
    The main driver program for the robotic leader-follower software.
    """
    tag = TagRecognition(marker_length=0.025)
    vehicle = decide_role(tag.detect())

    if isinstance(vehicle, Follower):
        while True:
            vehicle.follow()
    else:
        while True:
            vehicle.lead()


if __name__ == '__main__':
    main()
