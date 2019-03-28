"""
camera

Author: Steven Dropiewski
"""
from os import path
import sys
import time

FILE_PATH = path.dirname(path.realpath(__file__))
SUNFOUNDER_PATH = "SunFounder_PiCar-V/remote_control/remote_control/driver"
sys.path.append(FILE_PATH + "/../" + SUNFOUNDER_PATH)

from picar.SunFounder_PCA9685 import Servo
from picar import filedb
import picar

class Camera:
    """
    Camera class to control panning and tilting.

    Creates camera object that can be operated on using set_pan and set_tilt.
    set_pan operates [0,180] degrees. set_tilt operates [0,150] degrees. The 
    current values for pan and tilt in degrees can be returned using the get_pan
    and get_tilt methods. To change the offset you can may use calibrate_pan
    and calibrate_tilt methods. The methods will automatically update the values
    in the config file. All method parameters take absolute degrees.
    
    :param bus_number: The bus number the hat connects to.
    :type bus_number: int
    """

    PAN_CHANNEL = 1
    """Channel on PiCar HATS that connects to pan servo."""
    TILT_CHANNEL = 2
    """Channel on PiCar HATS that connects to tilt servo."""
    MAX_PAN_DEGREE = 180
    """The maximum value to be written to pan servo (in degrees)."""
    MAX_TILT_DEGREE = 150
    """The maximum value to be written to tilt servo (in degrees)."""
    MIN_DEGREE = 0
    """The minimum value to be written to both pan and tilt servo (in degrees)."""
    MAX_CALI_DEGREE = 180
    """The maximum value to calibrate pan and tilt (in degrees)."""
    MIN_CALI_DEGREE = -180
    """The minimum value to calibrate pan or tilt (in degrees."""
    OFFSET_TO_SERVO = 0
    """The offset value passed to the servo object."""

    def __init__(self, bus_number=1):
        picar.setup()

        self._DB = filedb.fileDB(FILE_PATH + "/../" + SUNFOUNDER_PATH + "/config")

        self._pan_offset = float(self._DB.get('pan_offset', default_value=0))
        self._tilt_offset = float(self._DB.get('tilt_offset', default_value=0))

        self._pan_servo = Servo.Servo(self.PAN_CHANNEL,  
                                      bus_number=bus_number, 
                                      offset=self.OFFSET_TO_SERVO)
        self._tilt_servo = Servo.Servo(self.TILT_CHANNEL, 
                                       bus_number=bus_number, 
                                       offset=self.OFFSET_TO_SERVO)

        self._current_pan_angle = 0
        self._current_tilt_angle = 0


    def set_pan(self, degree):
        """
        Pans the camera.

        Controls the horizontal movement of the camera in [0, 180] degrees. 
        0 refers to the vehicle's right while 180 refers to the vehicle's left. 

        :param degree: The degree to set the pan servo to.
        :type degree: float
        """
        self._current_pan_angle = self.validate_degree(degree, 
                                                       self.MIN_DEGREE,
                                                       self.MAX_PAN_DEGREE)
        self._pan_servo.write(self.validate_degree(self._current_pan_angle + 
                                                   self._pan_offset,
                                                   self.MIN_DEGREE,
                                                   self.MAX_PAN_DEGREE))


    def calibrate_pan(self, degree):
        """
        Calibrates camera pan.

        Controls offset in [-180, 180] degrees for pan. Writes new offset value to
        'SunFounder_PiCar-V/remote_control/remote_control/driver/config' 
        to 'pan_offset'. 

        :param degree: The amount of degrees to add or subtract for calibration.
        :type degree: float
        """
        self._pan_offset = self.validate_degree(degree, self.MIN_CALI_DEGREE,
                                                        self.MAX_CALI_DEGREE)
        self._DB.set('pan_offset', self._pan_offset)


    def get_pan(self):
        """
        :return: The current pan angle (in degrees).
        :rtype: float
        """
        return self._current_pan_angle


    def set_tilt(self, degree):
        """
        Tilts the camera.

        Controls the vertical movement of the camera in [0, 150] degrees. 
        0 refers to frontfacing while 150 refers to 60 degrees past vertical
        rotating upward. 

        :param degree: The degree to set the tilt servo to.
        :type degree: float
        """
        self._current_tilt_angle = self.validate_degree(degree,
                                                        self.MIN_DEGREE,
                                                        self.MAX_TILT_DEGREE)
        self._tilt_servo.write(self.validate_degree(self._current_tilt_angle +
                                                    self._tilt_offset,
                                                    self.MIN_DEGREE,
                                                    self.MAX_TILT_DEGREE))


    def calibrate_tilt(self, degree):
        """
        Calibrates camera tilt.

        Controls offset in [-180, 180] degrees for tilt. Writes new offset value to
        'SunFounder_PiCar-V/remote_control/remote_control/driver/config'
        to 'tilt_offset'.

        :param degree: The amount of degrees to add or subtract for calibration.
        :type degree: float
        """
        self._tilt_offset = self.validate_degree(degree, self.MIN_CALI_DEGREE,
                                                         self.MAX_CALI_DEGREE)
        self._DB.set('tilt_offset', self._tilt_offset)


    def get_tilt(self):
        """
        :return: The current tilt angle (in degrees).
        :rtype: float
        """
        return self._current_tilt_angle


    def validate_degree(self, degree, min_degree, max_degree):
        """
        Takes input and restricts to specifcied min and max.

        Returns the value in the degree parameter that is bounded by the 
        min_degree and max_degree parameters.

        :param degree: The value to be bounded between min and max degree.
        :type degree: float

        :param min_degree: The lower bound of the validation.
        :type min_degree: float

        :param max_degree: the upper bound of the validation.
        :type max_degree: float

        :return: The value of degree bounded between the min and max parameters.
        :rtype: float
        """
        return max(min(max_degree, degree), min_degree)


    def test_pan(self):
        """
        Tests the panning of the camera

        sets the camera to 90 degrees then to right most value at 0 degrees. 
        Then pans the camera from right to left giving over the maximum
        values showing validation function working as intended, ending at 180 
        degrees. Then pans the camera from left to right ending at 0 degrees.
        resets the camera to 90 degrees.
        """
        self.set_pan(90)
        time.sleep(.2)
        self.set_pan(0)
        time.sleep(.2)
        print ("panning from right to left")
        for i in range (-20, 200, 2):
            self.set_pan(i)
            time.sleep(.04)

        print ("panning from left to right")
        for i in range (200, -20, -2):
            self.set_pan(i)
            time.sleep(.04)
        
        time.sleep(.2)
        self.set_pan(90)


def main():
    cam = Camera()
    cam.test_pan()

if __name__ == '__main__':
    main()

