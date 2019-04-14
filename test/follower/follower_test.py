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

        self._decision_left = -1
        self._decision_straight = 0
        self._decision_right = 1

        self._default_tag_data = {
                'x': 0,
                'z': 0,
                'direction': 0,
                'decision': 0,
                'yaw': 0
       }


    def test_detect_tag_found(self):
        img_src = self._pictures_dir + "straight_no_turn_5in.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertNotEqual(follower._tag_data, self._default_tag_data)


    def test_detect_tag_not_found(self):
        img_src = self._pictures_dir + "no_tag.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertEqual(follower._tag_data, self._default_tag_data)


    """
    def test_drive_distance_below_lower_bound(self):
        img_src = self._pictures_dir + "straight_no_turn_third_car_length.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertAlmostEqual(follower._speed, 0)


    def test_drive_distance_at_lower_bound(self):
        img_src = self._pictures_dir + "straight_no_turn_3in.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertEqual(follower._speed, 0)
    """


    def test_drive_distance_at_upper_bound(self):
        img_src = self._pictures_dir + "straight_no_turn_12in.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertTrue(0 < follower._speed <= Follower.FOLLOWER_MAX_SPEED)


    def test_drive_distance_above_upper_bound(self):
        img_src = self._pictures_dir + "straight_no_turn_12in.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()
        sleep(follower.CYCLE_TIME)
        follower.follow()

        self.assertTrue(0 < follower._speed <= Follower.FOLLOWER_MAX_SPEED,
                        "Follower speed was: %d" % follower._speed)


    def test_drive_distance_valid(self):
        img_src = self._pictures_dir + "straight_no_turn_5in.png"

        follower = Follower(test_img_src=img_src)
        follower.follow()

        self.assertEqual(follower._speed, LEADER_MAX_SPEED)



if __name__ == '__main__':
    unittest.main()
