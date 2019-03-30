"""
camera

Author: Steven Dropiewski
"""
import numpy as np
import time

ABSOLUTE = 1
RELATIVE = 0

from picar import filedb
from picar.SunFounder_PCA9685 import Servo
import picar


class Camera:
    """
    Creates a camera object that can be panned and tilted.

    The camera can pan in [0, 180] degrees and can tilt in [0, 150] degrees.
    The camera operates in absolute degrees default, but can be specified to
    work in realtive degrees on object creation.

    :param bus_number: The bus number of the servos.
    :type bus_number: int

    :param pan_channel: Pan servo's I2C channel.
    :type pan_channel: int

    :param tilt_channel: Tilt servo's I2C channel.
    :type tilt_channel: int

    :param camera_type: Does the camera function in absolute or relative angles.
    :type camera_type: int
    """

    MAX_PAN_DEGREE = 180
    """The maximum value to be written to pan servo."""
    MAX_TILT_DEGREE = 150
    """The maximum value to be written to tilt servo."""
    MIN_DEGREE = 0
    """The minimum value to be written to both pan and tilt servo."""
    MAX_PAN_CALI_DEGREE = 180
    """The maximum value to calibrate pan."""
    MAX_TILT_CALI_DEGREE = 150
    """The maximum value to calibrate tilt."""
    MIN_PAN_CALI_DEGREE = -180
    """The minimum value to calibrate pan."""
    MIN_TILT_CALI_DEGREE = -150
    """The minimum value to calibrate tilt."""


    def __init__(self, bus_number=1, pan_channel=1, tilt_channel=2,
                                                    camera_type=ABSOLUTE):
        offset = 0

        self._db = filedb.fileDB("config")
        self._pan_offset = int(self._db.get('pan_offset', default_value=0))
        self._tilt_offset = int(self._db.get('tilt_offset', default_value=0))

        self._pan_servo = Servo.Servo(pan_channel, bus_number=bus_number,
                                                   offset=offset)
        self._tilt_servo = Servo.Servo(tilt_channel, bus_number=bus_number,
                                                     offset=offset)

        self._camera_type = ABSOLUTE if camera_type is not RELATIVE else RELATIVE

        self._current_pan_angle = 90
        self._current_tilt_angle = 0


    def pan(self, degree):
        """
        Pans the camera.

        Controls the horizontal movement of the camera in [0, 180] degrees.
        0 refers to the vehicle's right while 180 refers to the vehicle's left.
        The degrees will be clamped to [0, 180].

        :param degree: The number of degrees.
        :type degree: int
        """
        if self._camera_type == ABSOLUTE:
            self._current_pan_angle = np.clip(degree, self.MIN_DEGREE,
                                                      self.MAX_PAN_DEGREE)

        else:
            self._current_pan_angle = np.clip(degree + self._current_pan_angle,
                                                       self.MIN_DEGREE,
                                                       self.MAX_PAN_DEGREE)

        self._pan_servo.write(np.clip(self._current_pan_angle +
                                      self._pan_offset,
                                      self.MIN_DEGREE,
                                      self.MAX_PAN_DEGREE))


    def calibrate_pan(self, degree):
        """
        Calibrates the camera's panning servo.

        Writes a new pan offset value to the config file and changes the current
        pan offset. The calibration value can be negative.

        :param degree: The number of degrees.
        :type degree: int
        """
        if self._camera_type == ABSOLUTE:
            self._pan_offset = int(np.clip(degree, self.MIN_PAN_CALI_DEGREE,
                                                   self.MAX_PAN_CALI_DEGREE))
        else:
            self._pan_offset = int(np.clip(degree + self._pan_offset,
                                                    self.MIN_PAN_CALI_DEGREE,
                                                    self.MAX_PAN_CALI_DEGREE))

        self._db.set('pan_offset', self._pan_offset)


    def get_pan_angle(self):
        """
        Gets the current pan angle of the camera.

        :return: The current pan angle (in degrees).
        :rtype: int
        """
        return self._current_pan_angle


    def tilt(self, degree):
        """
        Tilts the camera.

        Controls the vertical movement of the camera in [0, 150] degrees.
        0 is directly in front of the car, 90 faces upwards, and 150 faces the
        Raspberry Pi. The degrees will be clamped to [0, 150].

        :param degree: The number of degrees.
        :type degree: int
        """
        if self._camera_type == ABSOLUTE:
            self._current_tilt_angle = np.clip(degree, self.MIN_DEGREE,
                                                       self.MAX_TILT_DEGREE)
        else:
            self._current_tilt_angle = np.clip(degree + self._current_tilt_angle,
                                                        self.MIN_DEGREE,
                                                        self.MAX_TILT_DEGREE)

        self._tilt_servo.write(np.clip(self._current_tilt_angle +
                                       self._tilt_offset,
                                       self.MIN_DEGREE,
                                       self.MAX_TILT_DEGREE))


    def calibrate_tilt(self, degree):
        """
        Calibrates the camera's tilting servo.

        Writes a new tilt offset value to the config file and changes the current
        tilt offset. The calibration value can be negative.

        :param degree: The number of degrees.
        :type degree: int
        """
        if self._camera_type == ABSOLUTE:
            self._tilt_offset = int(np.clip(degree, self.MIN_TILT_CALI_DEGREE,
                                                    self.MAX_TILT_CALI_DEGREE))
        else:
            self._tilt_offset = int(np.clip(degree + self._tilt_offset,
                                                     self.MIN_TILT_CALI_DEGREE,
                                                     self.MAX_TILT_CALI_DEGREE))

        self._db.set('tilt_offset', self._tilt_offset)


    def get_tilt_angle(self):
        """
        Gets the current tilt angle of the camera.

        :return: The current tilt angle (in degrees).
        :rtype: int
        """
        return self._current_tilt_angle


def main():
    """
    Demonstrates the camera's panning and tilting functionality.

    Creates a camera object and pans from 0 to 180, then from 180 to 0. The
    camera then tilts from 0 to 150, then 150 to 0.
    """
    camera_smoothing = 0.05
    picar.setup()
    camera = Camera()

    # Tests camera pan.
    print "Panning left."
    for i in range(0, 181, 2):
        camera.pan(i)
        time.sleep(camera_smoothing)

    print "Panning right."
    for i in range(180, -1, -2):
        camera.pan(i)
        time.sleep(camera_smoothing)

    # Resetting Pan.
    camera.pan(90)
    time.sleep(camera_smoothing)

    # Tests camera tilt.
    print "Tilting up."
    for i in range(0, 151, 2):
        camera.tilt(i)
        time.sleep(camera_smoothing)

    print "Tilting down."
    for i in range(150, -1, -2):
        camera.tilt(i)
        time.sleep(camera_smoothing)

    # Resetting camera for relative pan.
    cam.pan(0)
    time.sleep(camera_smoothing)

    # Remaking object in relative style.
    camera = None
    camera = Camera(camera_type = RELATIVE)

    print "Testing relative pan left."
    for i in range(0, 90, 1):
        camera.pan(2)
        time.sleep(camera_smoothing)

    print "Testing relative pan right."
    for i in range(0, 90, 1):
        camera.pan(-2)
        time.sleep(camera_smoothing)

    # Return camera to the center.
    camera.pan(-90)
    time.sleep(camera_smoothing)

if __name__ == '__main__':
    main()

