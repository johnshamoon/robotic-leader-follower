"""
inputcontroller

Author: John Shamoon
"""
from fcntl import ioctl
import array
import struct


class InputController:
    """
    Module used to get input from an Xbox One S controller.

    Assumes the device is /dev/input/js0.

    Recognized Buttons:
        1) Left Stick X and Y
        2) Right Stick Z and Rotation Z
        3) Left and Right Triggers
        4) Left and Right Buttons
        5) D-Pad Up, Left, Down, and Right
        6) A, B, X, and Y
        7) Start/Select Buttons
        8) Left and Right Stick Buttons

    :param debug: Enabling debug causes get_input() to print values.
    :type debug: bool
    """

    AXIS_CODES = {
        0x00 : 'left_stick_x',
        0x01 : 'left_stick_y',
        0x02 : 'right_stick_z',
        0x05 : 'right_stick_rotation_z',
        0x09 : 'right_trigger',
        0x0a : 'left_trigger',
        0x10 : 'dpad_left_right',
        0x11 : 'dpad_up_down',
    }
    """Linux axis codes from input-event-codes.h."""

    BUTTON_CODES = {
        0x130 : 'a',
        0x131 : 'b',
        0x132 : 'x',
        0x133 : 'y',
        0x134 : 'left_button',
        0x135 : 'right_button',
        0x136 : 'select_button',
        0x137 : 'start_button',
        0x138 : 'left_stick_button',
        0x139 : 'right_stick_button',
    }
    """Linux button codes from input-event-codes.h."""

    JSIOCGNAME = 0x80006a13
    """Gets the device's identifier string."""
    JSIOCGAXES = 0x80016a11
    """Gets the device's number of axes."""
    JSIOCGBUTTONS = 0x80016a12
    """Gets the device's number of buttons."""
    JSIOCGAXMAP = 0x80406a32
    """Gets the device's axis mapping."""
    JSIOCGBTNMAP = 0x80406a34
    """Gets the device's button mapping."""
    FORMAT = "IhBB"
    """
    Format to unpack a struct. Unsigned int, short, unsigned short, unsigned
    short.
    """

    EV_KEY = 0x01
    """Button event type."""
    EV_REL = 0x02
    """Axis event type."""

    AXIS_CALIBRATION = 32767.0
    """Calibrates axes to be in (-32767.0, 32767.0)"""
    DEVICE_NAME_MAX_LENGTH = 0x64
    """Device name can be at most 64 bytes."""
    DEVICE_NAME_BUFFER = 0x10000
    AXIS_MAP_BUFFER = 0x40
    BUTTON_MAP_BUFFER = 0x200


    def __init__(self, debug=False):
        self.js = open('/dev/input/js0', 'rb')
        self.axis_states = {}
        self.button_states = {}

        self.axis_map = []
        self.button_map = []
        self.debug = debug

        # Device name (64 unsigned chars)
        if self.debug:
            buf = array.array('b', [0] * self.DEVICE_NAME_MAX_LENGTH)
            ioctl(self.js, self.JSIOCGNAME + (self.DEVICE_NAME_BUFFER * len(buf)), buf)
            js_name = buf.tostring().decode('unicode-escape')
            print("Joystick Name: %s" % js_name)

        # Number of axes
        buf = array.array('B', [0])
        ioctl(self.js, self.JSIOCGAXES, buf)
        num_axes = buf[0]

        # Number of buttons
        buf= array.array('B', [0])
        ioctl(self.js, self.JSIOCGBUTTONS, buf)
        num_buttons = buf[0]

        # Axis Map
        buf = array.array('B', [0] * self.AXIS_MAP_BUFFER)
        ioctl(self.js, self.JSIOCGAXMAP, buf)
        for axis in buf[:num_axes]:
            axis_name = self.AXIS_CODES.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0

        # Button Map
        buf = array.array('H', [0] * self.BUTTON_MAP_BUFFER)
        ioctl(self.js, self.JSIOCGBTNMAP, buf)
        for btn in buf[:num_buttons]:
            button_name = self.BUTTON_CODES.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(button_name)
            self.button_states[button_name] = 0


    def get_input(self):
        """
        Takes input from /dev/input/js0 and returns a pair of (code, value).

        If a button is being pressed, value is 1. When the button stops being
        pressed, state is 0. If a button is not being pressed, the code will be
        -1.

        If an axis is being used, the value will be in [-1, 1]. When the input
        on the axis stops, the code is -1 and the position is -2.

        :return: A code and a value representing the linux
                             button/axis code and its value.
        :rtype: string, float

        :return: A code when the input button/axis is not being used anymore.
        :rtype: int, int
        """
        # Read 8 bytes: 2 for the type, 2 for the code, 4 for the value.
        event = self.js.read(8)
        if event:
            time, position, code, value = struct.unpack(self.FORMAT, event)
            # Buttons
            if code == self.EV_KEY:
                button = self.button_map[value]
                if button:
                    self.button_states[button] = position
                if self.debug:
                    if position:
                        print "%s pressed" % (button)
                    else:
                        print "%s released" % (button)
                else:
                    return button, position
            # Axes
            elif code == self.EV_REL:
                axis = self.axis_map[value]
                if axis:
                    axis_position = position / self.AXIS_CALIBRATION
                    self.axis_states[axis] = axis_position
                    if self.debug:
                        print "%s: %.3f" % (axis, axis_position)
                    else:
                        return axis, axis_position
            else:
                return -1, -1


def main():
    """
    Instantiates an InputController object with debugging enabled and
    continuously calls InputController.get_input().
    """
    controller = InputController(debug=True)
    while True:
        controller.get_input()


if __name__ == '__main__':
    main()
