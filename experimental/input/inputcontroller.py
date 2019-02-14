from fcntl import ioctl
import array
import struct


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
    7) Start Button
    8) Left and Right Stick Buttons
"""
class InputController:
    # Linux input codes from input-event-codes.h
    axis_codes = {
        0x00 : 'left_stick_x',
        0x01 : 'left_stick_y',
        0x02 : 'right_stick_z',
        0x05 : 'right_stick_rotation_z',
        0x09 : 'right_trigger',
        0x0a : 'left_trigger',
        0x10 : 'dpad_left_right',
        0x11 : 'dpad_up_down',
    }

    button_codes = {
        0x130 : 'a',
        0x131 : 'b',
        0x133 : 'x',
        0x134 : 'y',
        0x136 : 'left_button',
        0x137 : 'right_button',
        0x13b : 'start_button',
        0x13d : 'left_stick_button',
        0x13e : 'right_stick_button',
    }

    AXIS_CALIBRATION = 32767.0
    JSIOCGNAME = 0x80006a13
    JSIOCGAXES = 0x80016a11
    JSIOCGBUTTONS = 0x80016a12
    JSIOCGAXMAP = 0x80406a32
    JSIOCGBTNMAP = 0x80406a34
    FORMAT = 'IhBB'  # unsigned int, short, unsigned short * 2
    EV_KEY = 0x01
    EV_REL = 0x02

    DEVICE_NAME_MAX_LENGTH = 0x64
    DEVICE_NAME_BUFFER = 0x10000
    AXIS_MAP_BUFFER = 0x40
    BUTTON_MAP_BUFFER = 0x200

    js = open('/dev/input/js0', 'rb')
    axis_states = {}
    button_states = {}

    axis_map = []
    button_map = []

    debug = False


    def __init__(self, debug=False):
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
            axis_name = self.axis_codes.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0

        # Button Map
        buf = array.array('H', [0] * self.BUTTON_MAP_BUFFER)
        ioctl(self.js, self.JSIOCGBTNMAP, buf)
        for btn in buf[:num_buttons]:
            button_name = self.button_codes.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(button_name)
            self.button_states[button_name] = 0


    """
    Takes input from /dev/input/js0.

    Returns a pair of (code, state). If the button is being pressed, state is
    true. When the button stops being pressed, state is false. If a button is
    not being pressed, the code will be -1.
    """
    def getButtonInput(self):
        # Read 8 bytes: 2 for the type, 2 for the code, 4 for the value.
        event = self.js.read(8)
        if event:
            time, type, code, value = struct.unpack(self.FORMAT, event)
            # Ignore initial states
            if code & 0x80:
                if self.debug:
                    print("Initial State: ", end="")
                else:
                    return -1, False

            # Buttons
            if code & self.EV_KEY:
                button = self.button_map[value]
                if button:
                    self.button_states[button] = type
                if self.debug:
                    if type:
                        print("%s pressed" % (button))
                    else:
                        print("%s released" % (button))
                else:
                    return button, type


    """
    Takes input from /dev/input/js0.

    Returns a pair of (code, axis position). If the input is on an axis, the
    axis position will be in [-1, 1]. When the input on the axis stops, the
    code is -1 and the axis position is -2.
    """
    def getAxisInput(self):
        # Read 8 bytes: 2 for the type, 2 for the code, 4 for the value.
        event = self.js.read(8)
        if event:
            time, type, code, value = struct.unpack(self.FORMAT, event)
            # Ignore initial states
            if code & 0x80:
                if self.debug:
                    print("Initial State: ", end="")
                else:
                    return -1, -2

            if code & self.EV_REL:
                axis = self.axis_map[value]
                if axis:
                    axis_position = type / self.AXIS_CALIBRATION
                    self.axis_states[axis] = axis_position
                    if self.debug:
                        print("%s: %.3f" % (axis, axis_position))
                    else:
                        return axis, axis_position


if __name__ == '__main__':
    controller = InputController(debug=True)
    while True:
        controller.getButtonInput()
        controller.getAxisInput()
