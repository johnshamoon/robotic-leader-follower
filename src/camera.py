"""
camera

Author: Steven Dropiewski
"""
from time import sleep
import numpy as np

from picar import filedb
from picar.SunFounder_PCA9685 import Servo
import picar

ABSOLUTE = 1
"""The value set to identify absolute degrees."""
RELATIVE = 0
"""The value set to identify relative degrees."""


class Camera:
    """
    Creates a camera object that can be panned and tilted.

    The camera can pan in [0, 180] degrees and can tilt in [0, 150] degrees.
    The camera operates in absolute degrees by default, but can be specified to
    work in relative degrees during object creation.

    :param bus_number: The bus number of the servos.
    :type bus_number: int

    :param pan_channel: Pan servo's I2C channel.
    :type pan_channel: int

    :param tilt_channel: Tilt servo's I2C channel.
    :type tilt_channel: int

    :param camera_type: Camera.ABSOLUTE or Camera.RELATIVE angles.
    :type camera_type: int
    """

    MAX_PAN_DEGREE = 180
    """The maximum value that the camera can pan."""
    MAX_TILT_DEGREE = 150
    """The maximum value that the camera can tilt."""
    MIN_PAN_TILT_DEGREE = 0
    """The minimum value that the camera can pan and tilt."""
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
        # The value to set Servo object offset to.
        offset = 0

        self._db = filedb.fileDB("config")
        self._pan_offset = int(self._db.get('pan_offset', default_value=0))
        self._tilt_offset = int(self._db.get('tilt_offset', default_value=0))

        self._pan_servo = Servo.Servo(pan_channel, bus_number=bus_number,
                                                   offset=offset)
        self._tilt_servo = Servo.Servo(tilt_channel, bus_number=bus_number,
                                                     offset=offset)

        self._camera_type = RELATIVE if camera_type is RELATIVE else ABSOLUTE

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
            self._current_pan_angle = np.clip(degree, self.MIN_PAN_TILT_DEGREE,
                                                      self.MAX_PAN_DEGREE)

        else:
            self._current_pan_angle = np.clip(degree + self._current_pan_angle,
                                                       self.MIN_PAN_TILT_DEGREE,
                                                       self.MAX_PAN_DEGREE)

        self._pan_servo.write(np.clip(self._current_pan_angle
                                      + self._pan_offset,
                                      self.MIN_PAN_TILT_DEGREE,
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
            self._current_tilt_angle = np.clip(degree, self.MIN_PAN_TILT_DEGREE,
                                                       self.MAX_TILT_DEGREE)
        else:
            self._current_tilt_angle = np.clip(degree + self._current_tilt_angle,
                                                        self.MIN_PAN_TILT_DEGREE,
                                                        self.MAX_TILT_DEGREE)

        self._tilt_servo.write(np.clip(self._current_tilt_angle
                                       + self._tilt_offset,
                                       self.MIN_PAN_TILT_DEGREE,
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


    def reset_camera(self):
        """
        Resets the camera to default position.

        Sets the camera pan to 90 and the tilt to 0.
        """
        self._current_pan_angle = 90
        self._current_tilt_angle = 0

        self._pan_servo.write(np.clip(self._current_pan_angle
                                      + self._pan_offset,
                                      self.MIN_PAN_TILT_DEGREE,
                                      self.MAX_PAN_DEGREE))
        self._tilt_servo.write(np.clip(self._current_tilt_angle
                                       + self._tilt_offset,
                                       self.MIN_PAN_TILT_DEGREE,
                                       self.MAX_TILT_DEGREE))


def main():
    """
    Demonstrates the camera's panning and tilting functionality.

    Creates a camera object using absolute degrees and pans from 0 to 180, then
    from 180 to 0. The camera then tilts from 0 to 150, then 150 to 0.
    Then creates a camera object using relavtive degrees and pans from 0 to 180,
    then from 180 to 0. The camera then tilts from 0 to 150, then 150 to 0.
    camera_delay is used to allow smooth camera movement in small distances.
    camera_delay_long is used to allow the camera to move long distances fully.
    """
    camera_delay = 0.05
    camera_delay_long = 0.10
    picar.setup()

    # Creates a Camera object with absolute degrees (default).
    camera = Camera()
    print "Testing absolute camera degrees."

    # Moves the camera to the right for panning.
    camera.pan(0)
    sleep(camera_delay_long)

    print "Panning left."
    for i in range(0, 181, 2):
        camera.pan(i)
        sleep(camera_delay)

    print "Panning right."
    for i in range(180, -1, -2):
        camera.pan(i)
        sleep(camera_delay)

    # Moves the camera to the center for tilting.
    camera.reset_camera()
    sleep(camera_delay_long)

    print "Tilting up."
    for i in range(0, 151, 2):
        camera.tilt(i)
        sleep(camera_delay)

    print "Tilting down."
    for i in range(150, -1, -2):
        camera.tilt(i)
        sleep(camera_delay)

    # Creates a Camera object with relative degrees.
    camera = Camera(camera_type=RELATIVE)
    print "Testing relative camera degrees."

    # Moves the camera to the right for panning.
    camera.pan(-90)
    sleep(camera_delay_long)

    print "Panning left."
    for i in range(90):
        camera.pan(2)
        sleep(camera_delay)

    print "Panning right."
    for i in range(90):
        camera.pan(-2)
        sleep(camera_delay)

    # Moves the camera to the center for tilting.
    camera.reset_camera()
    sleep(camera_delay_long)

    print "Tilting up."
    for i in range(75):
        camera.tilt(2)
        sleep(camera_delay)

    print "Tilting down."
    for i in range(75):
        camera.tilt(-2)
        sleep(camera_delay)


if __name__ == '__main__':
    main()

