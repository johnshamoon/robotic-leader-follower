import subprocess

"""
The method is_connected takes the output of bt_check.sh and returns a boolean value.
The method is_connected is called with one arguement, the bluetooth address of the paired device.
"""
def is_connected(BluetoothAddress):
    BTADDR = BluetoothAddress
    # This calls the bt_check and gets a return value based on 
    # the exit value in bt_check.sh
    if subprocess.call(['./bt_check.sh', BTADDR]) == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
