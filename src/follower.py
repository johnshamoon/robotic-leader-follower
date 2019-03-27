import sys
from os import getcwd
from time import time
sys.path.append("../SunFounder_PiCar-V/remote_control/remote_control/driver")

from camera import Camera
from picar import back_wheels, front_wheels
import picar

from tagrec import TagRecognition
import numpy as np

"""
Autonomous follower vehicle to follow another vehicle.
Takes input from camera and autonomously follows another vehicle with an ARTag
mounted at the rear-center of the leader vehicle.
"""
class Follower:
    def __init__(self):
        # Car length
        self.MAX_DISTANCE = 0.28
        self.MIN_DISTANCE = self.MAX_DISTANCE / 3
        self.FOLLOWER_MAX_SPEED = 100
        self.LEADER_MAX_SPEED = self.FOLLOWER_MAX_SPEED - 25
        self.MAX_TAG_LOSS_TIME = 0.5
        self.INCREASE_SPEED_CYCLE_TIME = 0.1

        picar.setup()

        db_file = getcwd() + "/../SunFounder_PiCar-V/remote_control/remote_control/driver/config"
        self._fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self._bw = back_wheels.Back_Wheels(debug=False, db=db_file)

        self._fw.ready()
        self._bw.ready()

        self._fw.calibration()

        self._camera = Camera()
        self.reset_camera()

        self._tag = TagRecognition(marker_length=0.025)
        self._speed = 0

        self._distance = 0
        self._turn_angle = 0
        self._decision = 0
        self._yaw = 0

        self._tag_lost_time = 0
        self._speed_cycle_time = time()

        self.camera_angle_offset = 0

        self.STRAIGHT_ANGLE = 90


    """
    Drives the vehicle forward and avoids collisions with recognized objects.
    Manages the wheel speed to avoid collisions depending on the distance to
    the recognized object.
    """
    def drive(self):
        # If the vehicle is too close to the object, significantly decreese
        # speed.
        if self._distance <= self.MIN_DISTANCE:
            self._speed = 0
        elif self.MIN_DISTANCE < self._distance <= (self.MIN_DISTANCE * 2):
            # If we are in range of the leader vehicle, match the leader
            # vehicle's speed.This will keep the distance between the ego
            # vehicle and the leader vehicle.
            self._speed = self.LEADER_MAX_SPEED
        else:
            if (((time() - self._speed_cycle_time) > self.INCREASE_SPEED_CYCLE_TIME)
                and (self._speed + 1 <= self.FOLLOWER_MAX_SPEED)):
                # If the ego vehicle is not in the minimum distance for
                # INCREASE_SPEED_CYCLE_TIME, increase the speed and reset the
                # timer.
                self._speed += 1
                self._speed_cycle_time = time()

        self._bw.speed = self._speed
        self._bw.forward()


    """
    Stops the vehicle.
    """
    def stop(self):
        self._bw.speed = 0
        self._bw.forward()


    """
    Turn the wheels and pans the camera towards the last recognized object.
    """
    def turn(self):
        self.convert_camera_angle()
        self.pan_camera()

        if self.STRAIGHT_ANGLE - self.DEADZONE < self._turn_angle:
            self._fw.turn(self._turn_angle + self.camera_angle_offset) 
        elif self.STRAIGHT_ANGLE + self.DEADZONE > self._turn_angle:
            self._fw.turn(self._turn_angle - self.camera_angle_offset)

    
    """
    Follows the tag by panning camera towards the same direction as the wheels.
    """
    def pan_camera(self):

        if self._turn_angle < self.STRAIGHT_ANGLE - self.DEADZONE:
            self.turn_camera_left(self._turn_angle)
            self.camera_angle_offset = self._camera.current_pan - 90

        elif self._turn_angle > self.STRAIGHT_ANGLE + self.DEADZONE:
            self.turn_camera_right(self._turn_angle)
            self.camera_angle_offset = np.abs(self._camera.current_pan - 90)
 

    """
    Definitions for turning the camera left and right.
    Turn Left/Right functions from the Camera class only takes Steps.
    """
    def turn_camera_left(self, angle):
        self._camera.turn_left(self.angle_to_step())
    
    def turn_camera_right(self, angle):
        self._camera.turn_right(self.angle_to_step())

    
    """
    Definition for converting angles to steps.
    Takes the angle property and converts into steps where 1 step is 5 degrees.
    """
    def angle_to_step(self):
        return (self._turn_angle/self._camera.PAN_STEP)


    """
    Converts the camera's angle scale to the same scale as the wheels.
    The camera reports objects directly in front of it as 90 degrees. Everything
    to the left of center is negative ranging from [-45, -90) with -45 being the
    leftmost angle. Everything to the right of center is positive ranging from
    (90, 135] with 135 being the rightmost angle.
    The wheels turn on a range of [45, 135] with 45 being the rightmost, 135
    being the leftmost, and 90 being center.
    """
    def convert_camera_angle(self):
        if self._decision == -1:
            self._turn_angle = np.abs(self._yaw - 90)
        elif self._decision == 1:
            self._turn_angle = 90 + self._yaw
        else:
            self._turn_angle = 90


    """
    Resets the camera to the default position.
    The default position is tilted to 120 degrees and panned to 90 degrees.
    """
    def reset_camera(self):
        self._camera.turn_down(120)
        self._camera.pan_servo.write(90)


    """
    Detects an ARTag and gets the object's data.
    If an ARTag is detected, the object's distance and turning angle will be
    updated and detect() will return True. If an ARTag is not detected, detect()
    will return False.
    """
    def detect(self):
        obj_data = self._tag.detect()
        detected = False

        if obj_data:
            detected = True
            self._distance = obj_data['z']
            self._turn_angle = np.degrees(obj_data['direction'])
            self._decision = obj_data['decision']
            self._yaw = obj_data['yaw']

        return detected


    """
    Follow an ARTag if one is found.
    If an ARTag is detected, the follower vehicle will turn towards it and
    manage speed to avoid collisions. If an ARTag is not detected, the vehicle
    will stop.
    """
    def follow(self):
        if self.detect():
            self.drive()
            self.turn()
            self._tag_lost_time = 0
        else:
            if not self._tag_lost_time:
                self._tag_lost_time = time()
            elif self._tag_lost_time >= self.MAX_TAG_LOSS_TIME:
                self.stop()


def main():
    follower = Follower()
    while True:
        follower.follow()


if __name__ == '__main__':
    main()