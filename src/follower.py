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

from leader import MAX_SPEED as LEADER_MAX_SPEED
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
            self._speed = LEADER_MAX_SPEED
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
        """Turn the wheels towards the last recognized object."""
        self.convert_camera_angle()
        self._fw.turn(self._turn_angle)


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
