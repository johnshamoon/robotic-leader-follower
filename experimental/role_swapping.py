"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.

Authors: Zein Youssef and Steven Dropiewski
"""
from time import sleep
import os

from bluetoothctl import Bluetoothctl
from follower import Follower
from leader import Leader
from tagrec import TagRecognition


def is_controller_connected():
    """
    Determines if a Bluetooth controller is connected to /dev/input/js0.

    :return: True if a device is connected and False if not.
    :rtype: Boolean
    """
    return os.path.exists('/dev/input/js0')


def disconnect_and_remove_device(bt, bt_addr):
    """
    Disconnects and removes a controller from Bluetooth.

    :param bt: The object used to send Bluetooth commands.
    :type bt: Bluetoothctl

    :param bt_addr: The Bluetooth address of the device to disconnect from
                    and remove.
    :type bt_addr: string
    """
    bt.disconnect(bt_addr)
    sleep(Follower.CYCLE_TIME)
    if any(d['mac_address'] == bt_addr for d in bt.get_paired_devices()):
        bt.remove(bt_addr)


def main():
    """
    The main driver program for the robotic leader-follower software.
    """
    tag = TagRecognition()
    bt = Bluetoothctl()
    BT_ADDR = "5C:BA:37:26:6D:9A"

    # If an ARTag is detected, the vehicle will become a follower.
    # If an ARTag is not detected, the vehicle will become a leader.
    if tag.detect():
        follower = Follower()
        while True:
            follower.follow()
    else:
        if not is_controller_connected():
            # If a controller is not connected, remove it to avoid problems
            # connecting with it again.
            disconnect_and_remove_device(bt, BT_ADDR)
            bt.start_scan()

            while not is_controller_connected():
                bt.connect(BT_ADDR)
                sleep(Follower.CYCLE_TIME)

        leader = Leader()
        while True:
            leader.lead()


if __name__ == '__main__':
    main()

