"""
bluetoothctl

Linux Bluetooth wrapper.

Originally written by Egor Fedorov.
Copyright (c) 2015, Emlid Limited.

Modified and improved by John Shamoon.
"""
import pexpect
import subprocess
import time


class BluetoothctlError(Exception):
    """
    Bluetoothctl exception class.

    The exception is raised when bluetoothctl fails to start.
    """
    pass


class Bluetoothctl:
    """
    A wrapper for bluetoothctl.

    Provides Bluetooth capabilities.
    """

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl")
        self.child.setecho = False


    def get_output(self, command, pause = 0):
        """Run a command in a bluetoothctl prompt.

        :param command: The command to send the bluetoothctl prompt.
        :type command: string

        :param pause: The time to pause after the command (default: 0)
        :type pause: float

        :raises BluetoothctlError: If the command failed to run.

        :return: Output of command as a list of lies.
        :rtype: List of strings.
        """
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")


    def start_scan(self):
        """
        Start scanning for new Bluetooth devices.

        :return: None if the command failed to run.
        :rtype: None
        """
        try:
            out = self.get_output("scan on")
        except BluetoothctlError, e:
            print(e)
            return None


    def stop_scan(self):
        """
        Stop scanning for new Bluetooth devices.

        :return: None if the command failed to run.
        :rtype: None
        """
        try:
            out = self.get_output("scan off")
        except BluetoothctlError, e:
            print(e)
            return None


    def make_discoverable(self):
        """
        Make the current device discoverable.

        :return: None if the command failed to run.
        :rtype: None
        """
        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError, e:
            print(e)
            return None


    def parse_device_info(self, info_string):
        """
        Parse a string corresponding to a device.

        :param info_string: String containing the device information.
        :type info_string: string

        :return: Device information as a dictionary.
        :rtype: Dictionary containing "bt_address" and "name" as keys.
        """
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "bt_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device


    def get_available_devices(self):
        """
        Gets a list of paired and discoverable devices.

        :return: None if the command failed to run.
        :rtype: None

        :return: A list of tuples.
        :rtype: List of tuples of strings
        """
        try:
            out = self.get_output("devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices


    def get_paired_devices(self):
        """
        Gets the list of paired devices.

        :return: None if the command failed to run.
        :rtype: None

        :return: A list of tuples.
        :rtype: List of tuples of strings
        """
        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices


    def get_discoverable_devices(self):
        """
        Gets the list of discoverable devices.

        :return: The list of discoverable devices that are not currently paired
                 to the device.
        :rtype: List of strings
        """
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]


    def get_device_info(self, bt_address):
        """
        Gets the device info by Bluetooth address.

        :param bt_address: The Bluetooth address of the device.
        :type bt_address: string

        :return: None if the command failed to run.
        :rtype: None

        :return: The device information.
        :rtype: string
        """
        try:
            out = self.get_output("info " + bt_address)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            return out


    def pair(self, bt_address):
        """
        Pair with a device by Bluetooth address.

        :param bt_address: The Bluetooth address of the device.
        :type bt_address: string

        :return: None if the command failed to run.
        :rtype: None

        :return: True if the device paired, False otherwise.
        :rtype: boolean
        """
        try:
            out = self.get_output("pair " + bt_address, 4)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success


    def remove(self, bt_address):
        """
        Remove a paired device by Bluetooth address.

        :param bt_address: The Bluetooth address of the device.
        :type bt_address: string

        :return: None if the command failed to run.
        :rtype: None

        :return: True if the device was removed, False otherwise.
        :rtype: boolean
        """
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + bt_address, 3)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success


    def connect(self, bt_address):
        """
        Connect to a device by Bluetooth address.

        :param bt_address: The Bluetooth address of the device.
        :type bt_address: string

        :return: None if the command failed to run.
        :rtype: None

        :return: True if the device connected, False otherwise.
        :rtype: boolean
        """
        try:
            out = self.get_output("connect " + bt_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success


    def disconnect(self, bt_address):
        """
        Disconnect from a device by Bluetooth address.

        :param bt_address: The Bluetooth address of the device.
        :type bt_address: string

        :return: None if the command failed to run.
        :rtype: None

        :return: True if the device disconnected, False otherwise.
        :rtype: boolean
        """
        try:
            out = self.get_output("disconnect " + bt_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success

def main():
    """
    Instantiates a Bluetoothctl object, scans for devices, and prints the
    discoverable devices.
    """
    print("Initializing Bluetooth...")
    bt = Bluetoothctl()
    print("Ready!")

    bt.start_scan()
    print("Scanning for 10 seconds...")
    for i in range(0, 10):
        print(i)
        time.sleep(1)

    print(bt.get_discoverable_devices())


if __name__ == "__main__":
    main()

