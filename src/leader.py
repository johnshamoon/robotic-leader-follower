"""
leader

Author: John Shamoon
"""
import numpy as np

from inputcontroller import InputController

from log import Log

from picar import back_wheels, front_wheels
import picar

MAX_SPEED = 45
"""The maximum speed of the leader vehicle."""


class Leader:
    """
    Leader vehicle class.

    Takes input from /dev/input/js0 and directs the vehicle. To turn left or
    right, use the d-pad. To drive forward, use the right trigger. To drive
    backward, use the left trigger.

    :param test_mode: Test mode. Disables movements (off by default).
    :type test_mode: boolean
    """

    STRAIGHT_ANGLE = 90
    """The angle that the hardware associates as straight."""


    def __init__(self, test_mode=False):
        self._test_mode = False if test_mode is False else True
        self._controller = InputController()

        db_file = "config"
        picar.setup()

        self.fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=db_file)

        self.bw.ready()
        self.fw.ready()

        self.fw.calibration()

        log = Log('leader')

        self._tag_data = {
                'speed': 0,
                'turn_angle': 0,
        }


 def set_speed(self, position):
        """
        Sets the speed of the vehicle based on controller input.

        If the position is -1, the speed will be 0. If position is between (-1,1),
        the speed will increase as the position goes to 1. If the position is 1,
        the speed will be LEADER.MAX_SPEED.
        
        :param position: The value of the button input.
        :type position: float
        """
        try:
            position = np.clip(float(position), -1.0, 1.0)
            speed = int(MAX_SPEED * ((position + 1) / 2))
        except (ValueError, TypeError), e:
            speed = 0

        if not self._test_mode:
            self.bw.speed = speed

        return speed


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


    def turn(self, position):
        """
        Turns the wheels based on controller input.

        If position is -1, the wheels turn left. If position is 1, the wheels
        turn right. Otherwise, the wheels turn straight.

        :param position: The value returned from InputController.get_input().
        :type position: float

        :return: The turn angle.
        :rtype: float

        :return: None if position is not a number.
        :rtype: None
        """
        try:
            position = np.clip(float(position), -1.0, 1.0)
            turn_angle = self.STRAIGHT_ANGLE + (self.fw.turning_max * position)
            if not self._test_mode:
                self.fw.turn(turn_angle)
            return turn_angle
        except (ValueError, TypeError), e:
            return None


    def lead(self):
        """
        Controls a leader vehicle.

        Moves the leader vehicle based on controller input.
        """
        code, position = self._controller.get_input()
        if code == 'right_trigger':
            self._tag_data['speed'] = self.set_speed(position)
            self.drive()
        if code == 'left_trigger':
            self._tag_data['speed'] = self.set_speed(position)
            self.reverse()
        if code == 'dpad_left_right' or code == 'left_stick_x':
            self._tag_data['turn_angle'] = self.turn(code, position)

        log.write_to_file(leader._tag_data)


def main():
    """
    Instantiates a Leader object and continuously calls Leader.lead().
    """
    leader = Leader()
    while True:
        leader.lead()


if __name__ == '__main__':
    main()
