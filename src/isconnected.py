import subprocess

"""
The method is_connected takes the output of bt_check.sh and returns a boolean value.
The method is_connected is called with one arguement, the bluetooth address of the paired device.
"""
def is_connected(BluetoothAddress):
    BTADDR = BluetoothAddress
    # This calls the isconnected.sh and gets a return value based on 
    # the exit value in isconnected.sh
    if subprocess.call(['./isconnected.sh', BTADDR]) == 1:
        return True
    else:
        return False
