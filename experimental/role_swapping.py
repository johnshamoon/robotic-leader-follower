"""
Experimental script for role swapping.

Authors: Zein Youssef
"""
FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../src")

from bluetoothctl import Bluetoothctl
from follower import Follower
from leader import Leader
from tagrec import TagRecognition

import os
import subprocess
from time import sleep


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
    tag = TagRecognition()
    bt = Bluetoothctl()
    BT_ADDR = "5C:BA:37:26:6D:9A"

    # If an ARTag is detected, the vehicle will become a follower.
    # If an ARTag is not detected, the vehicle will become a leader.
    if tag.detect():
        vehicle = Follower()
    else:
        if not is_controller_connected():
            # If a controller is not connected, remove it to avoid problems
            # connecting with it again.
            disconnect_and_remove_device(bt, BT_ADDR)
            bt.start_scan()

            while not is_controller_connected():
                bt.connect(BT_ADDR)
                sleep(Follower.CYCLE_TIME)

        vehicle = Leader()

    # This loop makes the vehicle move. If the vehicle sees an ARTag then
    # it is a follower vehicle, otherwise it is a leader vehicle.
    timer_set = False
    start_time = time.time()

    while True:
        tag_visible = tag.detect()
        if isinstance(vehicle, Leader):
            vehicle.lead()

            if tag_visible:
                while is_controller_connected():
                    bt.disconnect('5C:BA:37:26:6D:9A')
                    sleep(Follower.CYCLE_TIME)
                vehicle = Follower()
        else:
            vehicle.follow()
            if tag_visible:
                timer_set = False
            elif not timer_set:
                start_time = time.time()
                timer_set = True

            if (time.time() - start_time) > 5 and timer_set:
                timer_set = False

                disconnect_and_remove_device(bt,BT_ADDR)
                bt.start_scan()
                bt.connect('5C:BA:37:26:6D:9A')
                sleep(Follower.CYCLE_TIME)

                if is_controller_connected():
                    vehicle = Leader()
                else:
                    start_time = time.time()
                    timer_set = True


if __name__ == '__main__':
    main()
