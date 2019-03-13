"""
camera

Author: Steven Dropiewski
"""
from os import path
import sys

FILE_PATH = path.dirname(path.realpath(__file__))
SUNFOUNDER_PATH = "SunFounder_PiCar-V/remote_control/remote_control/driver"
sys.path.append(FILE_PATH + "/../" + SUNFOUNDER_PATH)

from picar.SunFounder_PCA9685 import Servo
from picar import filedb

class Camera:
    """
    Camera class to control panning and tilting.

    Creates camera object that can be operated on using set_pan and set_tilt.
    set_pan operates [0,180] degrees. set_tilt operates [0,150] degrees. The 
    current values for pan and tilt in degrees can be returned using the get_pan
    and get_tilt functions. If the offset needs to be changed it is located in 
    "/../SunFounder_PiCar-V/remote_control/remote_control/driver/config"under
    pan_offset and tilt_offset. 
    """

    PAN_CHANNEL = 1
    """Channel on PiCar HATS that connects to pan servo."""
    TILT_CHANNEL = 2
    """Channel on PiCar HATS that connects to tilt servo."""
    MAX_PAN_DEGREE = 180
    """The maximum value to be passed to pan servo (in degrees)."""
    MAX_TILT_DEGREE = 150
    """The maximum value to be passed to tilt servo (in degrees)."""
    MIN_DEGREE = 0
    """The minimum value to be passed to both pan and tilt servo (in degrees)."""
    MAX_CALI_DEGREE = 180
    """The maximum value to calibrate pan and tilt (in degrees)."""
    MIN_CALI_DEGREE = -180
    """The minimum value to calibrate pan or tilt (in degrees."""
    OFFSET_TO_SERVO = 0
    """The offset value handed to the servo object."""

    def __init__(self, bus_number=1):
        self._DB = filedb.fileDB(FILE_PATH + "/../" + SUNFOUNDER_PATH + "/config")
        self._pan_offset = int(self._DB.get('pan_offset', default_value=0))
        self._tilt_offset = int(self._DB.get('tilt_offset', default_value=0))
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
        """
        self._current_pan_angle = self.validate_degree(degree, 
                                                       self.MIN_DEGREE,
                                                       self.MAX_PAN_DEGREE)
        self._pan_servo.write(self.validate_degree(self._current_pan_angle +
                                                   self>_pan_offset,
                                                   self.MIN_DEGREE,
                                                   self.MAX_PAN_DEGREE))


    def calibrate_pan(self, degree):
        """
        Calibrates camera pan.

        Controls offset in [-180, 180] degrees for pan. Writes new offset value to
        'SunFounder_PiCar-V/remote_control/remote_control/driver/config' 
        to 'pan_offset'. 
        """
        self._pan_offset = self.validate_degree(degree, self.MIN_CALI_DEGREE,
                                                        self.MAX_CALI_DEGREE)
        self._db.set('pan_offset', self._pan_offset)


    def get_pan(self):
        """Returns current pan angle in [0, 180] degrees."""
        return self._current_pan_angle


    def set_tilt(self, degree):
        """
        Tilts the camera.

        Controls the vertical movement of the camera in [0, 150] degrees. 
        0 refers to frontfacing while 150 refers to 60 degrees past vertical
        rotating upward. 
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
        """
        self._tilt_offset = self.validate_degree(degree, self.MIN_CALI_DEGREE,
                                                         self.MAX_CALI_DEGREE)
        self._db.set('tilt_offset', self._tilt_offset)


    def get_tilt(self):
        """Returns the current tilt angle in [0, 150] degrees."""
        return self._current_tilt_angle
 
 
    def validate_degree(self, degree, min_degree, max_degree):
        """
        Takes input and restricts to specifcied min and max.

        Returns the value in the degree parameter that is bounded by the 
        min_degree and max_degree parameters.
        """
        return max(min(max_degree, degree), min_degree)

    #def main():


if __name__ == '__main__':
    main()

