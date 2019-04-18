from os import path
from time import sleep

import numpy
import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from follower import Follower

from leader import MAX_SPEED as LEADER_MAX_SPEED

class FollowerTest(unittest.TestCase):
    def setUp(self):
        self._pictures_dir = FILE_PATH + "/../res/tag_pictures/"

        self._default_tag_data = {
                'x': 0,
                'z': 0,
                'direction': 0,
                'decision': 0,
                'yaw': 0
       }


    def test_detect_tag_found(self):
        img_src = self._pictures_dir + "straight_no_turn_5in.jpg"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertNotEqual(follower._tag_data, self._default_tag_data)


    def test_detect_tag_not_found(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertEqual(follower._tag_data, self._default_tag_data)


    def test_drive_distance_below_lower_bound(self):
        img_src = self._pictures_dir + "straight_no_turn_third_car_length.jpg"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertAlmostEqual(follower._speed, 0)


    def test_drive_distance_at_lower_bound(self):
        img_src = self._pictures_dir + "straight_no_turn_3in.jpg"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertEqual(follower._speed, 0)


    def test_drive_distance_valid(self):
        img_src = self._pictures_dir + "straight_no_turn_5in.jpg"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertEqual(follower._speed, LEADER_MAX_SPEED)


    def test_opencv_to_wheels_straight_decision(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(90, follower.opencv_to_wheels(0, 10))


    def test_opencv_to_wheels_left_decision_at_bound(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(45, follower.opencv_to_wheels(-1, 90))


    def test_opencv_to_wheels_left_decision_below_bound(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(45, follower.opencv_to_wheels(-1, 100))


    def test_opencv_to_wheels_right_decision_at_bound(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(135, follower.opencv_to_wheels(1, 45))


    def test_opencv_to_wheels_right_decision_below_bound(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(135, follower.opencv_to_wheels(1, 46))


    def test_opencv_to_wheels_string_params(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(90, follower.opencv_to_wheels("decision", "yaw"))


    def test_opencv_to_wheels_none_params(self):
        img_src = self._pictures_dir + "no_tag.jpg"

        follower = Follower(test_img_src=img_src)
        self.assertEqual(90, follower.opencv_to_wheels(None, None))


if __name__ == '__main__':
    unittest.main()
