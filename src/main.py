"""
Script to determine leader and follower roles.

Takes input from the camera to determine if the current vehicle
should lead or follow based on whether or not there exists an ARTag
in front of the vehicle.

If an ARTag exists, the vehicle will become a follower vehicle.
If an ARTag does not exist, the vehicle will become the leader vehicle.

Authors: Zein Youssef and Steven Dropiewski
"""
<<<<<<< HEAD
=======
from time import sleep
import os

from bluetoothctl import Bluetoothctl
from follower import Follower
from leader import Leader
from tagrec import TagRecognition

import os
import subprocess
import time


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
"""
This function calls the ./bt_toggle script with the specified
command and address
"""
def bt_toggle(command, address):
    subprocess.call(['./bt_toggle.sh', command, address])


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

        isLeader = True
    bt_address = '5C:BA:37:26:6D:9A'
    bl = Bluetoothctl()
    BT_ADDRESS = '5C:BA:37:26:6D:9A'

    # If an ARTag is detected, there is a vehicle ahead of this vehicle so it will follow.
    # If an ARTag is not detected, no vehicle is present so this vehicle will be a leader.
    if tag.detect():
        while is_controller_connected():
            bl.disconnect('5C:BA:37:26:6D:9A')
        vehicle = Follower()
    else:
        while not is_controller_connected():
            bl.connect('5C:BA:37:26:6D:9A')
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
                    bl.disconnect('5C:BA:37:26:6D:9A')
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
                bl.connect('5C:BA:37:26:6D:9A')
          
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
