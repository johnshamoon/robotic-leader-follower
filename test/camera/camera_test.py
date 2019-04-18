from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from camera import Camera

class CameraTest(unittest.TestCase):
    def setUp(self):
        self._db = filedb.fileDB("config")


    def tearDown(self):
        self._db.set('pan_offset', 0)
        self._db.set('tilt_offset', 0)


    def test_pan_left_absolute(self):
        camera = Camera()
        camera.pan(120)

        self.assertEqual(camera._current_pan_angle, 120)


    def test_pan_left_absolute_at_bound(self):
        camera = Camera()
        camera.pan(180)

        self.assertEqual(camera._current_pan_angle, 180)


    def test_pan_left_absolute_beyond_bound(self):
        camera = Camera()
        camera.pan(181)

        self.assertEqual(camera._current_pan_angle, 180)


    def test_pan_right_absolute(self):
        camera = Camera()
        camera.pan(60)

        self.assertEqual(camera._current_pan_angle, 60)


    def test_pan_right_absolute_at_bound(self):
        camera = Camera()
        camera.pan(0)

        self.assertEqual(camera._current_pan_angle, 0)


    def test_pan_right_absolute_beyond_bound(self):
        camera = Camera()
        camera.pan(-1)

        self.assertEqual(camera._current_pan_angle, 0)


    def test_pan_left_relative(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(30)

        self.assertEqual(camera._current_pan_angle, 120)


    def test_pan_left_relative_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(90)

        self.assertEqual(camera._current_pan_angle, 180)


    def test_pan_left_relative_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(91)

        self.assertEqual(camera._current_pan_angle, 180)


    def test_pan_right_relative(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(-30)

        self.assertEqual(camera._current_pan_angle, 60)


    def test_pan_right_relative_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(-90)

        self.assertEqual(camera._current_pan_angle, 0)


    def test_pan_right_relative_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(-91)

        self.assertEqual(camera._current_pan_angle, 0)


    def test_tilt_up_absolute(self):
        camera = Camera()
        camera.tilt(90)

        self.assertEqual(camera._current_tilt_angle, 90)


    def test_tilt_up_absolute_at_bound(self):
        camera = Camera()
        camera.tilt(150)

        self.assertEqual(camera._current_tilt_angle, 150)


    def test_tilt_up_absolute_beyond_bound(self):
        camera = Camera()
        camera.tilt(151)

        self.assertEqual(camera._current_tilt_angle, 150)


    def test_tilt_down_absolute(self):
        camera = Camera()
        camera.tilt(90)
        camera.tilt(60)

        self.assertEqual(camera._current_tilt_angle, 60)


    def test_tilt_down_absolute_at_bound(self):
        camera = Camera()
        camera.tilt(90)
        camera.tilt(0)

        self.assertEqual(camera._current_tilt_angle, 0)


    def test_tilt_down_absolute_beyond_bound(self):
        camera = Camera()
        camera.tilt(90)
        camera.tilt(-1)

        self.assertEqual(camera._current_tilt_angle, 0)


    def test_tilt_up_relative(self):
        camera = Camera(camera_type=RELATIVE)
        camera.tilt(90)

        self.assertEqual(camera._current_tilt_angle, 90)


    def test_tilt_up_relative_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.tilt(150)

        self.assertEqual(camera._current_tilt_angle, 150)


    def test_tilt_up_relative_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.tilt(151)

        self.assertEqual(camera._current_tilt_angle, 150)


    def test_tilt_down_relative(self):
        camera = Camera(camera_type=RELATIVE)
        camera.tilt(90)
        camera.tilt(-30)

        self.assertEqual(camera._current_tilt_angle, 60)


    def test_tilt_down_relative_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.tilt(90)
        camera.tilt(-90)

        self.assertEqual(camera._current_tilt_angle, 0)


    def test_tilt_down_relative_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.tilt(90)
        camera.tilt(-91)

        self.assertEqual(camera._current_tilt_angle, 0)


    def test_get_pan_angle(self):
        camera = Camera()
        camera.pan(90)

        self.assertEqual(camera._current_pan_angle, camera.get_pan_angle())


    def test_get_tilt_angle(self):
        camera = Camera()
        camera.tilt(90)

        self.assertEqual(camera._current_tilt_angle, camera.get_tilt_angle())


    def test_calibrate_pan_absolute_increase(self):
        camera = Camera()

        calbrate_pan_test(camera, 10, 10)


    def test_calibrate_pan_absolute_increase_at_bound(self):
        camera = Camera()

        calibrate_pan_test(camera, 180, 180)


    def test_calibrate_pan_absolute_increase_beyond_bound(self):
        camera = Camera()

        calibrate_pan_test(camera, 181, 180)


    def test_calibrate_pan_absolute_decrease(self):
        camera = Camera()

        calibrate_pan_test(camera, -10, -10)


    def test_calibrate_pan_absolute_decrease_at_bound(self):
        camera = Camera()

        calibrate_pan_test(camera, -180, -180)


    def test_calibrate_pan_absolute_decrease_beyond_bound(self):
        camera = Camera()

        calibrate_pan_test(camera, -181, -180)


    def test_calibrate_pan_realtive_increase(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_pan_test(camera, 10, 10)


    def test_calibrate_pan_realtive_increase_at_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_pan_test(camera, 180, 180)


    def test_calibrate_pan_realtive_increase_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_pan_test(camera, 181, 180)


    def test_calibrate_pan_realtive_decrease(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_pan_test(camera, -10, -10)


    def test_calibrate_pan_realtive_decrease_at_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_pan_test(camera, -180, -180)


    def test_calibrate_pan_realtive_decrease_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_pan_test(camera, -181, -180)


    def test_calibrate_tilt_increase_absolute(self):
        camera = Camera()

        calibrate_tilt_test(camera, 10, 10)


    def test_calibrate_tilt_absolute_increase_at_bound(self):
        camera = Camera()

        calibrate_tilt_test(camera, 150, 150)


    def test_calibrate_tilt_absolute_increase_beyond_bound(self):
        camera = Camera()

        calibrate_tilt_test(camera, 151, 150)


    def test_calibrate_tilt_decrease_absolute(self):
        camera = Camera()

        calibrate_tilt_test(camera, -10, -10)


    def test_calibrate_tilt_absolute_decrease_at_bound(self):
        camera = Camera()

        calibrate_tilt_test(camera, -150, -150)


    def test_calibrate_tilt_absolute_decrease_beyond_bound(self):
        camera = Camera()

        calibrate_tilt_test(camera, -151, -150)


    def test_calibrate_tilt_relative_increase(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_tilt_test(camera, 10, 10)


    def test_calibrate_tilt_relative_increase_at_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_tilt_test(camera, 150, 150)


    def test_calibrate_tilt_relative_increase_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_tilt_test(camera, 151, 150)


    def test_calibrate_tilt_relative_decrease(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_tilt_test(camera, -10, -10)


    def test_calibrate_tilt_relative_decrease_at_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_tilt_test(camera, -150, -150)


    def test_calibrate_tilt_relative_decrease_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)

        calibrate_tilt_test(camera, -151, -150)


    def test_reset_camera_absolute(self):
        camera = Camera()
        camera.pan(150)
        camera.tilt(90)

        camera.reset_camera()

        self.assertEqual(camera._current_pan_angle, 90)
        self.assertEqual(camera._current_tilt_angle, 0)


    def test_reset_camera_realtive(self):
        camera = Camera(camera_type=RELATIVE)
        camera.pan(60)
        camera.tilt(90)

        camera.reset_camera()

        self.assertEqual(camera._current_pan_angle, 90)
        self.assertEqual(camera._current_tilt_angle, 0)


def calibrate_pan_test(camera, calibration_value, expected_value):
    camera.calibrate_pan(calibration_value)
    offset = int(self._db.get('pan_offset', default_value=0))
    self.assertEqual(camera._pan_offset, expected_value)
    self.assertEqual(offset, expected_value)


def calibrate_tilt_test(camera, calibration_value, expected_value):
    camera.calibrate_tilt(calibration_value)
    offset = int(self._db.get('tilt_offset', default_value=0))
    self.assertEqual(camera._tilt_offset, expected_value)
    self.assertEqual(offset, expected_value)


if __name__ == '__main__':
    unittest.main()
