import sys
from os import getcwd
sys.path.append("../SunFounder_PiCar-V/remote_control/remote_control/driver")

from camera import Camera
from picar import back_wheels, front_wheels
import picar

from tagrec import TagRecognition
import numpy as np

"""
Follower vehicle class.

Takes input from camera and follows another vehicle.
"""
class Follower:

    def __init__(self):
        self.MAX_DISTANCE = 0.28
        self.MIN_DISTANCE = self.MAX_DISTANCE / 3
        self.FOLLOWER_MAX_SPEED = 100
        self.LEADER_MAX_SPEED = self.FOLLOWER_MAX_SPEED - 25
        self.CAMERA_MIN_PAN = 30
        self.CAMERA_MAX_PAN = 120

        self.db_file = getcwd() + "/../SunFounder_PiCar-V/remote_control/remote_control/driver/config"
        picar.setup()

        self.fw = front_wheels.Front_Wheels(debug=False, db=self.db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=self.db_file)

        self.bw.ready()
        self.fw.ready()

        self.fw.calibration()

        self.camera = Camera()
        self.reset_camera()

        self.tag = TagRecognition()
        self.cycle = 0
        self.decision = 0
        self.speed = 0

        self.camera_offset = 0


    def drive(self):
        self.bw.speed = self.speed
#        self.bw.speed = 0
        self.bw.forward()


    def stop(self):
        self.bw.speed = 0
        self.bw.forward()


    def turn_angle(self, angle, decision):
        if decision == -1: # [45, 90]
            angle *= -1
        elif decision == 1: # [90, 135]
            angle = 180 - angle
        else:
            angle = 90
        self.fw.turn(angle)


    def reset_camera(self):
        self.camera.tilt_servo.write(120)
        self.camera.tilt_servo.write(0)
        self.camera.turn_down(120)
        self.camera.pan_servo.write(90)


    def follow(self):
        obj_data = self.tag.detect()
        if not obj_data:
            self.stop()
            return

        distance = obj_data['z']
        angle = obj_data['direction']
        angle *= (180 / np.pi)
        decision = obj_data['decision']

        if distance < self.MIN_DISTANCE:
            self.speed = 0
        elif distance >= self.MAX_DISTANCE:
            self.speed = 100
        else:
            self.speed = self.LEADER_MAX_SPEED

        self.drive()
        self.turn_angle(angle, decision)


def main():
    follower = Follower()
    while True:
        follower.follow()

if __name__ == '__main__':
    main()
