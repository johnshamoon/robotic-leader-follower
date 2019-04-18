"""
follower

Author: John Shamoon
"""
from time import time
import numpy as np
import os

from picar import back_wheels, front_wheels
import picar

from leader import MAX_SPEED as LEADER_MAX_SPEED
from camera import Camera
from tagrec import TagRecognition


class Follower:
    """
    Autonomous follower vehicle to follow another vehicle.

    Takes input from camera and autonomously follows another vehicle with an
    ARTag mounted at the rear-center of the leader vehicle.

    :param test_img_src: Path to an image. Used to bypass the camera feed and
                         follow ARTags from images instead. Used primarily for
                         testing. Disabled by default.
    :type test_img_src: str

    :raise IOError: Thrown if test_img_src is not a file.
    """

    MAX_DISTANCE = 0.28
    """Length of a car from a SunFounder PiCar-V kit (in meters)."""
    MIN_DISTANCE = MAX_DISTANCE / 3
    """One third of the length of a car from a SunFounder PiCar-V kit (in meters)."""
    FOLLOWER_MAX_SPEED = 55
    """
    The max speed of the leader vehicle. The leader is slower than the follower
    to allow the follower to catch up.
    """
    CYCLE_TIME = 0.1
    """The cycle time of the system."""

    def __init__(self, test_img_src=None):
        self._test_mode = False
        self._test_img_src = None
        if test_img_src:
            if os.path.isfile(test_img_src):
                self._test_mode = True
                self._test_img_src = test_img_src
            else:
                raise IOError("File does not exist.")

        picar.setup()

        db_file = "config"
        self._fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self._bw = back_wheels.Back_Wheels(debug=False, db=db_file)

        self._fw.ready()
        self._bw.ready()

        self._fw.calibration()

        self._camera = Camera()

        self._tag = TagRecognition(resolution=144, marker_length=0.025)
        self._speed = 0

        self._tag_data = {
                'x': 0,
                'z': 0,
                'direction': 0,
                'decision': 0,
                'yaw': 0
        }

        self._tag_lost_time = 0
        self._speed_cycle_time = time()
        self._turn_time = time()


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

        # If the vehicle is too close to the object, stop the vehicle.
        if self._tag_data['z'] <= self.MIN_DISTANCE:
            self._speed = 0
        elif self.MIN_DISTANCE < self._tag_data['z'] <= (self.MIN_DISTANCE * 2):
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

        if not self._test_mode:
            self._bw.speed = self._speed
            self._bw.forward()


    def stop(self):
        """Stops the vehicle."""
        self._bw.speed = 0
        self._bw.forward()


    def turn(self):
        """Turn the wheels towards the last recognized object."""
        turn_angle = self.opencv_to_wheels(self._tag_data['decision'],
                                           self._tag_data['yaw'])
        if not self._test_mode:
            self._fw.turn(turn_angle)


    def opencv_to_wheels(self, turn_decision, yaw):
        """
        Converts OpenCV's angle scale to the same scale as the wheels.

        OpenCV reports objects directly in front of it as 90 degrees.
        Everything to the left of center is negative ranging from [-45, -90)
        with -45 being the leftmost angle. Everything to the right of center is
        positive ranging from (90, 135] with 135 being the rightmost angle.

        The wheels turn on a range of [45, 135] with 45 being the rightmost, 135
        being the leftmost, and 90 being center.

        :param turn_decision: Where the leader vehicle is turning. -1 means the
                              leader is turning left, 1 means the leader is
                              turning right, and any other value means the
                              leader is not turning.
        :type turn_decision: int

        :param yaw: The yaw angle of the tag.
        :type yaw: float

        :return: The turn angle to the ARTag in [45, 135].
        """
        turn_angle = 90
        try:
            turn_decision = int(turn_decision)
            yaw = int(yaw)
        except (ValueError, TypeError), e:
            turn_decision = 0

        if turn_decision == -1:
            turn_angle = np.abs(yaw - 90)
        elif turn_decision == 1:
            turn_angle = 90 + yaw

        return np.clip(turn_angle, 45, 135)


    def detect(self):
        """
        Detects an ARTag and gets the object's data.

        If an ARTag is detected, the object's distance and turning angle will be
        updated and detect() will return True. If an ARTag is not detected,
        detect() will return False.

        :return: True if an ARTag is detected, False otherwise.
        :rtype: Boolean
        """
        if self._test_mode:
            tag_data = self._tag.detect(self._test_img_src)
        else:
            tag_data = self._tag.detect()
        detected = False

        if tag_data:
            detected = True
            self._tag_data = tag_data
            self._tag_data['direction'] = np.degrees(self._tag_data['direction'])

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
            if not self._turn_time:
                self._turn_time = time()
            elif (time() - self._turn_time) >= self.CYCLE_TIME:
                self.turn()
                self._turn_time = time()
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
