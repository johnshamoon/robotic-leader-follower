"""
follower

Author: John Shamoon
"""
from os import path
from time import time
import numpy as np
import sys

FILE_PATH = path.dirname(path.realpath(__file__))
SUNFOUNDER_PATH = "SunFounder_PiCar-V/remote_control/remote_control/driver"
sys.path.append(FILE_PATH + "/../" + SUNFOUNDER_PATH)

from camera import Camera
from picar import back_wheels, front_wheels
import picar

from tagrec import TagRecognition

class Follower:
    """
    Autonomous follower vehicle to follow another vehicle.

    Takes input from camera and autonomously follows another vehicle with an
    ARTag mounted at the rear-center of the leader vehicle.
    """

    MAX_DISTANCE = 0.28
    """Length of a car from a SunFounder PiCar-V kit (in meters)."""
    MIN_DISTANCE = MAX_DISTANCE / 3
    """One third of the length of a car from a SunFounder PiCar-V kit (in meters)."""
    FOLLOWER_MAX_SPEED = 100
    """The max speed of a car from a SunFounder PiCar-V kit."""
    LEADER_MAX_SPEED = FOLLOWER_MAX_SPEED - 25
    """
    The max speed of the leader vehicle. The leader is slower than the follower
    to allow the follower to catch up.
    """
    CYCLE_TIME = 0.1
    """The cycle time of the system."""

    def __init__(self):
        picar.setup()

        db_file = FILE_PATH + "/../" + SUNFOUNDER_PATH + "/config"
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
        self.WHEEL_MAX = 135
        self.WHEEL_MIN = 45
        self.DEADZONE_CAMERA = 7
        self.DEADZONE_WHEELS = 10


    def drive(self):
        """
        Drives forward and avoids forward collisions with recognized objects.
        Manages the speed to avoid collisions depending on the distance to the
        recognized object. If the recognized object is within MIN_DISTANCE, the
        speed will be set to 0. If the recognized object is outside of the
        MAX_DISTANCE, the speed will be set to FOLLOWER_MAX_SPEED. If the
        vehicle is within [MIN_DISTANCE, MAX_DISTANCE), the vehicle will match
        the leader vehicle's speed.
        """

        # If the vehicle is too close to the object, significantly decreese
        # speed.
        if self._distance <= self.MIN_DISTANCE:
            self._speed = 0
        elif self.MIN_DISTANCE < self._distance <= (self.MIN_DISTANCE * 2):
            # If we are in range of the leader vehicle, match the leader
            # vehicle's speed.This will keep the distance between the ego
            # vehicle and the leader vehicle.
            self._speed = self.LEADER_MAX_SPEED
        elif (((time() - self._speed_cycle_time) > self.CYCLE_TIME)
              and (self._speed + 1 <= self.FOLLOWER_MAX_SPEED)):
                # If the ego vehicle is not in the minimum distance for
                # CYCLE_TIME, increase the speed and reset the timer.
                self._speed += 1
                self._speed_cycle_time = time()

        self._bw.speed = self._speed
        self._bw.forward()


    def stop(self):
        """Stops the vehicle."""
        self._bw.speed = 0
        self._bw.forward()


    def turn(self):
        """
        Turn the wheels towards the last recognized object.
        """
        self.convert_camera_angle()
        self.pan_camera()

        if self.STRAIGHT_ANGLE + self.DEADZONE_WHEELS < self._turn_angle:
            # Left condition: when the turn angle is between 90 + deadzone and 135, turn the wheels at that angle plus the offset. 
            # If the turn angle is over the maximum wheel turn angle, set the turn angle to the wheel max.
            self._fw.turn(self._turn_angle + self.camera_angle_offset) 
            if self._turn_angle + self.camera_angle_offset > self.WHEEL_MAX:
              self._fw.turn(self.WHEEL_MAX)

        elif self.STRAIGHT_ANGLE - self.DEADZONE_WHEELS > self._turn_angle:
            # Right condition: when the turn angle is between 90 - deadzone and 45, turn the wheels at that angle minus the offset. 
            # If the turn angle is under the minimum wheel turn angle, set the turn angle to the wheel min.
            self._fw.turn(self._turn_angle - self.camera_angle_offset)
            if self._turn_angle - self.camera_angle_offset < self.WHEEL_MIN:
              self._fw.turn(self.WHEEL_MIN)


    def pan_camera(self):
        """
        Follows the tag by panning camera towards the same direction as the wheels.
        """
        if self._turn_angle < self.STRAIGHT_ANGLE - self.DEADZONE_CAMERA:
            # Left condition: If the turn angle is less than 90 - deadzone, turn the camera left. 
            # The offset is 90 - the current angle.
            self.turn_camera_left(self._turn_angle)
            self.camera_angle_offset = np.abs(90 - self._camera.current_pan)

        elif self._turn_angle > self.STRAIGHT_ANGLE + self.DEADZONE_CAMERA:
            # Right condition: If the turn angle is greater than 90 + deadzone, turn the camera right. 
            # The offset is the current angle - 90.
            self.turn_camera_right(self._turn_angle)
            self.camera_angle_offset = np.abs(self._camera.current_pan - 90)

        if self.camera_angle_offset == self.STRAIGHT_ANGLE or self.camera_angle_offset == self.WHEEL_MIN:
            # If the offset of the right or left offsets are equal to 90 or 45 respectively, turn the camera straight since the wheels will be straight.
            self._camera.current_pan = self.STRAIGHT_ANGLE
            self._camera.pan_servo.write(self._camera.current_pan)
            self._fw.turn(self._camera.current_pan)
 

    def turn_camera_left(self, angle):
        """
        Turns camera left. Camera API turn left function only takes steps.
        """
        self._camera.turn_left(self.angle_to_step())
    
    def turn_camera_right(self, angle):
        """
        Turns camera right. Camera API turn right function only takes steps.
        """
        self._camera.turn_right(self.angle_to_step())

    
    def angle_to_step(self):
        """
        Definition for converting angles to steps. 
        Takes the angle property and converts into steps where 1 step is 5 degrees.
        """
        return (self._turn_angle/self._camera.PAN_STEP) + 4

    
    def convert_camera_angle(self):
        """
        Converts the camera's angle scale to the same scale as the wheels.

        The camera reports objects directly in front of it as 90 degrees.
        Everything to the left of center is negative ranging from [-45, -90)
        with -45 being the leftmost angle. Everything to the right of center is
        positive ranging from (90, 135] with 135 being the rightmost angle.

        The wheels turn on a range of [45, 135] with 45 being the rightmost, 135
        being the leftmost, and 90 being center.
        """
        if self._decision == -1:
            self._turn_angle = np.abs(self._yaw - 90)
        elif self._decision == 1:
            self._turn_angle = 90 + self._yaw
        else:
            self._turn_angle = 90


    def reset_camera(self):
        """
        Resets the camera to the default position.

        The default position is tilted to 120 degrees and panned to 90 degrees.
        """
        self._camera.turn_down(120)
        self._camera.pan_servo.write(90)


    def detect(self):
        """
        Detects an ARTag and gets the object's data.

        If an ARTag is detected, the object's distance and turning angle will be
        updated and detect() will return True. If an ARTag is not detected,
        detect() will return False.

        :return: True if an ARTag is detected, False otherwise.
        :rtype: Boolean
        """
        obj_data = self._tag.detect()
        detected = False

        if obj_data:
            detected = True
            self._distance = obj_data['z']
            self._turn_angle = np.degrees(obj_data['direction'])
            self._decision = obj_data['decision']
            self._yaw = obj_data['yaw']

        return detected


    def follow(self):
        """
        Follow an ARTag if one is found.
        If an ARTag is detected, the follower vehicle will turn towards it and
        manage speed to avoid collisions. If an ARTag is not detected, the vehicle
        will stop.
        """
        if self.detect():
            self.drive()
            self.turn()
            self._tag_lost_time = 0
        else:
            if not self._tag_lost_time:
                self._tag_lost_time = time()
            elif (time() - self._tag_lost_time) >= self.CYCLE_TIME:
                self.stop()


def main():
    """Instantiates a Follower object and continously calls Follower.follow()."""
    follower = Follower()
    while True:
        follower.follow()


if __name__ == '__main__':
    main()