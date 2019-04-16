from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from camera import Camera

class CameraTest(unittest.TestCase):
    def setUp(self):
        self._db = filedb.fileDB("config")
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
        camera.calibrate_pan(10)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, 10)
        self.assertEqual(offset, 10)

    def test_calibrate_pan_absolute_increase_at_bound(self):
        camera = Camera()
        camera.calibrate_pan(180)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, 180)
        self.assertEqual(offset, 180)


    def test_calibrate_pan_absolute_increase_beyond_bound(self):
        camera = Camera()
        camera.calibrate_pan(181)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, 180)
        self.assertEqual(offset, 180)


    def test_calibrate_pan_absolute_decrease(self):
        camera = Camera()
        camera.calibrate_pan(-10)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, -10)
        self.assertEqual(offset, -10)


    def test_calibrate_pan_absolute_decrease_at_bound(self):
        camera = Camera()
        camera.calibrate_pan(-180)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, -180)
        self.assertEqual(offset, -180)


    def test_calibrate_pan_absolute_decrease_beyond_bound(self):
        camera = Camera()
        camera.calibrate_pan(-181)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, -180)
        self.assertEqual(offset, -180)


    def test_calibrate_pan_realtive_increase(self):
        camera = Camera(camera_type=RELATIVE)
        initial_pan_calibration = camera.pan_offset
        camera.calibrate_pan(10)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, initial_pan_calibration + 10)
        self.assertEqual(offset, initial_pan_calibration + 10)


    def test_calibrate_pan_realtive_increase_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_pan(180)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, 180)
        self.assertEqual(offset, 180)


    def test_calibrate_pan_realtive_increase_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_pan(181)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, 180)
        self.assertEqual(offset, 180)


    def test_calibrate_pan_realtive_decrease(self):
        camera = Camera(camera_type=RELATIVE)
        initial_pan_calibration = camera.pan_offset
        camera.calibrate_pan(-10)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, initial_pan_calibration - 10)
        self.assertEqual(offset, initial_pan_calibration - 10)


    def test_calibrate_pan_realtive_decrease_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_pan(-180)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, -180)
        self.assertEqual(offset, -180)


    def test_calibrate_pan_realtive_decrease_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_pan(-181)
        offset = int(self._db.get('pan_offset', default_value=0))

        self.assertEqual(camera._pan_offset, -180)
        self.assertEqual(offset, -180)


    def test_calibrate_tilt_increase_absolute(self):
        camera = Camera()
        camera.calibrate_tilt(10)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, 10)
        self.assertEqual(offset, 10)


    def test_calibrate_tilt_absolute_increase_at_bound(self):
        camera = Camera()
        camera.calibrate_tilt(150)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, 150)
        self.assertEqual(offset, 150)


    def test_calibrate_tilt_absolute_increase_beyond_bound(self):
        camera = Camera()
        camera.calibrate_tilt(151)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, 150)
        self.assertEqual(offset, 150)


    def test_calibrate_tilt_decrease_absolute(self):
        camera = Camera()
        camera.calibrate_tilt(-10)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, -10)
        self.assertEqual(offset, -10)


    def test_calibrate_tilt_absolute_decrease_at_bound(self):
        camera = Camera()
        camera.calibrate_tilt(-150)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, -150)
        self.assertEqual(offset, -150)


    def test_calibrate_tilt_absolute_decrease_beyond_bound(self):
        camera = Camera()
        camera.calibrate_tilt(-151)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, -150)
        self.assertEqual(offset, -150)


    def test_calibrate_tilt_relative_increase(self):
        camera = Camera(camera_type=RELATIVE)
        initial_tilt_calibration = camera.tilt_offset
        camera.calibrate_tilt(10)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, initial_tilt_calibration + 10)
        self.assertEqual(offset, initial_tilt_calibration + 10)


    def test_calibrate_tilt_relative_increase_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_tilt(150)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, 150)
        self.assertEqual(offset, 150)


    def test_calibrate_tilt_relative_increase_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_tilt(151)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, 150)
        self.assertEqual(offset, 150)


    def test_calibrate_tilt_relative_decrease(self):
        camera = Camera(camera_type=RELATIVE)
        initial_tilt_calibration = camera.tilt_offset
        camera.calibrate_tilt(-10)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, initial_tilt_calibration - 10)
        self.assertEqual(offset, initial_tilt_calibration - 10)


    def test_calibrate_tilt_relative_decrease_at_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_tilt(-150)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, -150)
        self.assertEqual(offset, -150)


    def test_calibrate_tilt_relative_decrease_beyond_bound(self):
        camera = Camera(camera_type=RELATIVE)
        camera.calibrate_tilt(-151)
        offset = int(self._db.get('tilt_offset', default_value=0))

        self.assertEqual(camera._tilt_offset, -150)
        self.assertEqual(offset, -150)


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


if __name__ == '__main__':
    unittest.main()
