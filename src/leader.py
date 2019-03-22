from os import path
import numpy as np
import sys

FILE_PATH = path.dirname(path.realpath(__file__))
SUNFOUNDER_PATH = "SunFounder_PiCar-V/remote_control/remote_control/driver"
sys.path.append(FILE_PATH + "/../" + SUNFOUNDER_PATH)

from inputcontroller import InputController

from picar import back_wheels, front_wheels
import picar


"""
Leader vehicle class.

Takes input from /dev/input/js0 and directs the vehicle. To turn left or right,
use the d-pad. To drive forward, use the right trigger. To drive backwards, use
the left trigger.
"""
class Leader:
    STRAIGHT_ANGLE = 89
    MAX_TURN_ANGLE = 45

    def __init__(self):
        self._controller = InputController()

        db_file = FILE_PATH + "/../" + SUNFOUNDER_PATH + "/config"
        picar.setup()

        self.fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=db_file)

        self.bw.ready()
        self.fw.ready()

        self.fw.calibration()


    # Determines if the car should be moving or not.
    def set_speed(self, position):
        if position == -1:
            speed = 0
        else:
            speed = 75
        self.bw.speed = speed


    def drive(self):
        self.bw.forward()


    def reverse(self):
        self.bw.backward()


    def turn_left(self):
        self.fw.turn_left()


    def turn_right(self):
        self.fw.turn_right()


    def turn_straight(self):
        self.fw.turn(self.STRAIGHT_ANGLE)


    def turn(self, code, position):
        if code == 'dpad_left_right':
            if position == -1:
                self.turn_left()
            elif position == 1:
                self.turn_right()
            else:
                self.turn_straight()
        elif code == 'left_stick_x':
            self.fw.turn(self.STRAIGHT_ANGLE + (self.MAX_TURN_ANGLE * position))


    def lead(self):
        code, position = self._controller.get_input()
        if code == 'right_trigger':
            self.set_speed(position)
            self.drive()
        if code == 'left_trigger':
            self.set_speed(position)
            self.reverse()
        if code == 'dpad_left_right' or code == 'left_stick_x':
            self.turn(code, position)


def main():
    leader = Leader()
    while True:
        leader.lead()


if __name__ == '__main__':
    main()
