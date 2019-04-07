"""
leader

Author: John Shamoon
"""
from os import path
import numpy as np
import sys

FILE_PATH = path.dirname(path.realpath(__file__))
SUNFOUNDER_PATH = "SunFounder_PiCar-V/remote_control/remote_control/driver"
sys.path.append(FILE_PATH + "/../" + SUNFOUNDER_PATH)

from inputcontroller import InputController

from picar import back_wheels, front_wheels
import picar

MAX_SPEED = 50
"""The maximum speed of the leader vehicle."""


class Leader:
    """
    Leader vehicle class.

    Takes input from /dev/input/js0 and directs the vehicle. To turn left or
    right, use the d-pad. To drive forward, use the right trigger. To drive
    backward, use the left trigger.
    """

    STRAIGHT_ANGLE = 90
    """The angle that the hardware associates as straight."""


    def __init__(self):
        self._controller = InputController()

        db_file = FILE_PATH + "/../" + SUNFOUNDER_PATH + "/config"
        self._mode = 'normal'
        picar.setup()

        self.fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=db_file)

        self.bw.ready()
        self.fw.ready()

        self.fw.calibration()


    def set_speed(self, position):
        """
        Sets the speed of the vehicle based on controller input.

        If the position is -1, the speed will be 0. If position is between (-1,1),
        the speed will increase as the position goes to 1. If the position is 1,
        the speed will be LEADER.MAX_SPEED.

        :param position: The value of the button input.
        :type position: int
        """
        if position == -1:
            speed = 0
        else:
            speed = int(MAX_SPEED * ((position + 1)/2))
        self.bw.speed = speed


    def drive(self):
        """
        Moves the vehicle forward.

        The vehicle moves forward at the last set speed.
        """
        self.bw.forward()


    def reverse(self):
        """
        Moves the vehicle backward.

        The vehicle moves backward at the last set speed.
        """
        self.bw.backward()


    def turn_left(self):
        """
        Turns the wheels to the left.

        The wheels are turned 45 degrees to the left (135 degrees).
        """
        self.fw.turn_left()


    def turn_right(self):
        """
        Turns the wheels to the right.

        The wheels are turned 45 degrees to the right (45 degrees).
        """
        self.fw.turn_right()


    def turn_straight(self):
        """
        Turns the wheels straight.

        Turns the wheels to 90 degrees.
        """
        self.fw.turn(self.STRAIGHT_ANGLE)


    def turn(self, code, position):
        """
        Turns the wheels based on controller input.

        If position is -1, the wheels turn left. If position is 1, the wheels
        turn right. Otherwise, the wheels turn straight.

        :param code: The code returned from InputController.get_input().
        :type code: string

        :param position: The value returned from InputController.get_input().
        :type position: float
        """
        if code == 'dpad_left_right':
            if position == -1:
                self.turn_left()
            elif position == 1:
                self.turn_right()
            else:
                self.turn_straight()
        elif code == 'left_stick_x':
            self.fw.turn(self.STRAIGHT_ANGLE + (self.fw.turning_max * position))


    def lead(self):
        """
        Controls a leader vehicle.

        Moves the leader vehicle based on controller input.
        """
        code, position = self._controller.get_input()
        if code == 'left_trigger' or code == 'right_trigger':
            self._mode = 'normal'

        elif code == 'x' and position == 1:
            if self._mode == 'demo 1':
                self._mode = 'normal'
            else:
                self._mode = 'demo 1'

        elif code == 'y' and position == 1:
            if self._mode == 'demo 2':
                self._mode = 'normal'
            else:
                self._mode = 'demo 2'

        elif code == 'b' and position == 1:
            if self._mode == 'demo 3':
                self._mode = 'normal'
            else:
                self._mode = 'demo 3'

        if self._mode == 'normal':
            if code == 'right_trigger':
                self.set_speed(position)
                self.drive()
            if code == 'left_trigger':
                self.set_speed(position)
                self.reverse()
            if code == 'dpad_left_right' or code == 'left_stick_x':
                self.turn(code, position)

        if self._mode == 'demo 1':
            self.demo1()

        if self._mode == 'demo 2':
            self.demo2()

        if self._mode == 'demo 3':
            self.demo3()


def main():
    """
    Instantiates a Leader object and continuously calls Leader.lead().
    """
    leader = Leader()
    while True:
        leader.lead()


if __name__ == '__main__':
    main()
