from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from tagrec import TagRecognition

class MainTest(unittest.TestCase):
    def setUp(self):
        self._pictures_dir = FILE_PATH + "/../res/tag_pictures/"


    def test_resolution_90p(self):
        tag = TagRecognition(resolution=90)

        self.assertEqual(tag._RESOLUTION, 90)


    def test_resolution_180p(self):
        tag = TagRecognition(resolution=180)

        self.assertEqual(tag._RESOLUTION, 180)


    def test_resolution_240p(self):
        tag = TagRecognition(resolution=240)

        self.assertEqual(tag._RESOLUTION, 240)


    def test_resolution_360p(self):
        tag = TagRecognition(resolution=360)

        self.assertEqual(tag._RESOLUTION, 360)


    def test_resolution_480p(self):
        tag = TagRecognition(resolution=480)

        self.assertEqual(tag._RESOLUTION, 480)


    def test_resolution_720p(self):
        tag = TagRecognition(resolution=720)

        self.assertEqual(tag._RESOLUTION, 720)


    def test_resolution_1080p(self):
        tag = TagRecognition(resolution=1080)

        self.assertEqual(tag._RESOLUTION, 1080)


    def test_resolution_unsupported(self):
        tag = TagRecognition(resolution=3840)

        self.assertEqual(tag._RESOLUTION, 90)


    def test_resolution_default(self):
        tag = TagRecognition()

        self.assertEqual(tag._RESOLUTION, 90)


    def test_deadzone_positive(self):
        tag = TagRecognition(dead_zone=1)

        self.assertEqual(tag._DEADZONE_RIGHT, 1)
        self.assertEqual(tag._DEADZONE_LEFT, -1)


    def test_deadzone_negative(self):
        tag = TagRecognition(dead_zone=-1)

        self.assertEqual(tag._DEADZONE_RIGHT, sys.maxsize)
        self.assertEqual(tag._DEADZONE_LEFT, -sys.maxsize)


    def test_deadzone_none(self):
        tag = TagRecognition(dead_zone=0)

        self.assertEqual(tag._DEADZONE_RIGHT, sys.maxsize)
        self.assertEqual(tag._DEADZONE_LEFT, -sys.maxsize)


    def test_deadzone_default(self):
        tag = TagRecognition()

        self.assertEqual(tag._DEADZONE_RIGHT, 1.45)
        self.assertEqual(tag._DEADZONE_LEFT, -1.45)


    def test_contrast_negative(self):
        tag = TagRecognition(contrast=-1)

        self.assertEqual(tag._CONTRAST, 0.1)


    def test_contrast_zero(self):
        tag = TagRecognition(contrast=0)

        self.assertEqual(tag._CONTRAST, 0.1)


    def test_contrast_lower_bound(self):
        tag = TagRecognition(contrast=0.1)

        self.assertEqual(tag._CONTRAST, 0.1)


    def test_contrast_lower(self):
        tag = TagRecognition(contrast=0.5)

        self.assertEqual(tag._CONTRAST, 0.5)


    def test_contrast_higher(self):
        tag = TagRecognition(contrast=2)

        self.assertEqual(tag._CONTRAST, 2)


    def test_contrast_upper_bound(self):
        tag = TagRecognition(contrast=101)

        self.assertEqual(tag._CONTRAST, 100)


    def test_contrast_default(self):
        tag = TagRecognition()

        self.assertEqual(tag._CONTRAST, 1)


    def test_brightness_outside_lower_bound(self):
        tag = TagRecognition(brightness=-128)

        self.assertEqual(tag._BRIGHTNESS, -127)


    def test_brightness_lower_bound(self):
        tag = TagRecognition(brightness=-127)

        self.assertEqual(tag._BRIGHTNESS, -127)


    def test_brightness_negative(self):
        tag = TagRecognition(brightness=-120)

        self.assertEqual(tag._BRIGHTNESS, -120)


    def test_brightness_zero(self):
        tag = TagRecognition(brightness=0)

        self.assertEqual(tag._BRIGHTNESS, 0)


    def test_brightness_positive(self):
        tag = TagRecognition(brightness=120)

        self.assertEqual(tag._BRIGHTNESS, 120)


    def test_brightness_upper_bound(self):
        tag = TagRecognition(brightness=127)

        self.assertEqual(tag._BRIGHTNESS, 127)


    def test_brightness_outside_upper_bound(self):
        tag = TagRecognition(brightness=128)

        self.assertEqual(tag._BRIGHTNESS, 127)


    def test_brightness_default(self):
        tag = TagRecognition()

        self.assertEqual(tag._BRIGHTNESS, 0)


    def test_tag_present(self):
        tag = TagRecognition()

        img_src = self._pictures_dir + "straight_no_turn_third_car_length.jpg"

        self.assertNotEqual(tag.detect(img_src=img_src), None)


    def test_tag_not_present(self):
        tag = TagRecognition()

        img_src = self._pictures_dir + "no_tag.jpg"

        self.assertEqual(tag.detect(img_src=img_src), None)


    def test_tag_x_left_side(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "left_no_turn_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['x'], -0.1, delta=0.06)


    def test_tag_x_middle(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "straight_no_turn_3in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['x'], 0.0, delta=0.06)


    def test_tag_x_right_side(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "right_no_turn_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['x'], 0.1, delta=0.06)


    def test_tag_z_close_range(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "straight_no_turn_3in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['z'], 0.0762, delta=0.06)


    def test_tag_z_medium_range(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "straight_no_turn_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['z'], 0.127, delta=0.06)


    def test_tag_z_far_range(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "straight_no_turn_12in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['z'], 0.3048, delta=0.15)


    def test_tag_direction_left_angle(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "left_no_turn_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['direction'], -1.25, delta=0.06)


    def test_tag_direction_center_angle(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "straight_no_turn_3in.jpg"

        self.assertTrue(-1.67 < tag.detect(img_src=img_src)['direction'] < 1.67)


    def test_tag_direction_right_angle(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "right_no_turn_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['direction'], 1.3, delta=0.06)


    def test_tag_decision_left(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "left_no_turn_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], -1)


    def test_tag_decision_center(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "tag_center.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], 0)


    def test_tag_decision_right(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "right_no_turn_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], 1)


    def test_tag_decision_outer_left_with_deadzone(self):
        tag = TagRecognition(marker_length=0.025, dead_zone=1.45)

        img_src = self._pictures_dir + "left_no_turn_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], -1)


    def test_tag_decision_inner_left_with_deadzone(self):
        tag = TagRecognition(marker_length=0.019, dead_zone=1.45)

        img_src = self._pictures_dir + "left_off_center_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], 0)


    def test_tag_decision_inner_center_with_deadzone(self):
        tag = TagRecognition(marker_length=0.025, dead_zone=1.45)

        img_src = self._pictures_dir + "straight_no_turn_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], 0)


    def test_tag_decision_inner_right_with_deadzone(self):
        tag = TagRecognition(marker_length=0.019, dead_zone=1.45)

        img_src = self._pictures_dir + "right_off_center_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], 0)


    def test_tag_decision_outer_right_with_deadzone(self):
        tag = TagRecognition(marker_length=0.025, dead_zone=1.45)

        img_src = self._pictures_dir + "right_no_turn_5in.jpg"

        self.assertEqual(tag.detect(img_src=img_src)['decision'], 1)


    def test_tag_yaw_left_side(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "right_sharp_turn_left_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['yaw'], 15, delta=5)


    def test_tag_yaw_center(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "tag_center.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['yaw'], 0, delta=5)


    def test_tag_yaw_right_side(self):
        tag = TagRecognition(marker_length=0.025)

        img_src = self._pictures_dir + "left_sharp_turn_right_5in.jpg"

        self.assertAlmostEqual(tag.detect(img_src=img_src)['yaw'], 5, delta=5)


if __name__ == '__main__':
    unittest.main()
