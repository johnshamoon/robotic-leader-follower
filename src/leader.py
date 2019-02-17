import sys
from os import getcwd
sys.path.append("../SunFounder_PiCar-V/remote_control/remote_control/driver")

from inputcontroller import InputController

from camera import Camera
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


    def __init__(self):
        self.controller = InputController()

        camera = Camera()
        camera.turn_down(120)
        self.db_file = getcwd() + "/../SunFounder_PiCar-V/remote_control/remote_control/driver/config"
        picar.setup()

        self.fw = front_wheels.Front_Wheels(debug=False, db=self.db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=self.db_file)

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
        self.fw.turn(STRAIGHT_ANGLE)


    def turn(self,position):
        if position == -1:
            self.turn_left()
        elif position == 1:
            self.turn_right()
        else:
            self.turn_straight()


def main():
    leader = Leader()
    controller = InputController()

    while True:
        code, position = controller.getInput()
        if code == 'right_trigger':
            leader.set_speed(position)
            leader.drive()
        if code == 'left_trigger':
            leader.set_speed(position)
            leader.reverse()
        if code == 'dpad_left_right':
            leader.turn(position)


if __name__ == '__main__':
    main()
