"""
tagrec

Author: Wisam Bunni
"""
import cv2
import cv2.aruco as ar
import numpy as np
import sys
import os


class TagRecognition():
    """
    Tag Recognition class.

    Takes input from the camera to look for an ARTag and returns useful
    information about the tag.

    :param resolution: The camera's resolution.
    :type resolution: int

    :param dead_zone: The dead zone to consider everything to be directly in
                      front of the camera.
    :type dead_zone: float

    :param marker_length: The square length of the ARTag in meters.
    :type marker_length: float

    :param contrast: The contrast multiplier.
                     A value in (0, 1) lowers the contrast and
                     a value in [1, 100] increases the contrast.
    :type contrast: float

    :param brightness: The brightness value in (-127, 127).
    :type brightness: int
    """

    RESOLUTIONS = {
            1080: [1920, 1080],
            720: [1280, 720],
            480: [720, 480],
            360: [480, 360],
            240: [426, 240],
            180: [320, 180],
            144: [176, 144],
            90: [160, 90]
    }
    """Pre-set resolutions."""

    _cap = cv2.VideoCapture(0)


    def __init__(self, resolution=90, dead_zone=1.45, marker_length=0.06,
            contrast=1, brightness=0):
        self._RESOLUTION = resolution if resolution in self.RESOLUTIONS else 90
        """The resolution of the camera feed."""
        self._MARKER_LENGTH = np.clip(marker_length, 0.01905, 0.0381)
        """The length of the ARTag in meters."""
        self._CONTRAST = np.clip(contrast, 0.1, 100)
        """The camera feed contrast multiplier."""
        self._BRIGHTNESS = np.clip(brightness, -127, 127)
        """The camera feed brightness."""

        # Handle a special case where the user requests to have no dead zones.
        if dead_zone <= 0:
            self._DEADZONE_RIGHT = sys.maxsize
            self._DEADZONE_LEFT = -sys.maxsize
        else:
            self._DEADZONE_RIGHT = abs(dead_zone)
            self._DEADZONE_LEFT = -self._DEADZONE_RIGHT

        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH,
                self.RESOLUTIONS[self._RESOLUTION][0])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT,
                self.RESOLUTIONS[self._RESOLUTION][1])

        self._corners = np.array([[0,0]] * 4)

        self._AR_DICT = ar.Dictionary_get(ar.DICT_6X6_250)
        self._PARAMETERS = ar.DetectorParameters_create()

        self._CALIBRATION_FILE = 'calibration.xml'
        self._CALIBRATION_PARAMS = cv2.FileStorage(self._CALIBRATION_FILE,
            cv2.FILE_STORAGE_READ)

        self._DIST_COEFFS = self._CALIBRATION_PARAMS.getNode('distCoeffs').mat()

        self._ret, self._frame = self._cap.read()
        self._size = self._frame.shape

        self._FOCAL_LENGTH = self._size[1]
        self._CENTER = (self._size[1]/2, self._size[0]/2)

        # Set up a camera matrix. This will allow to estimate the pose of the
        # ARTag.
        self._CAMERA_MATRIX = np.array(
            [[self._FOCAL_LENGTH, 0, self._CENTER[0]],
             [0, self._FOCAL_LENGTH, self._CENTER[1]],
             [0, 0, 1]], dtype='double'
        )

        self._tag_data = {
                'x': 0,
                'z': 0,
                'direction': 0,
                'decision': 0,
                'yaw': 0
        }


    def get_direction(self, object_x, object_z):
        """
        Gets the angle of the tag location with respect to the camera.

        :param object_x: The ARTag's location on the x-axis.
        :type object_x: float

        :param object_z: The ARTag's location on the z-axis.
        :type object_z: float

        :return: The current turn angle of the ARTag in radians.
        :rtype: float
        """
        try:
            turn_angle = np.arctan(object_z / object_x)
        except ZeroDivisionError:
            turn_angle = 90

        return turn_angle


    def make_decision(self, direction):
        """
        Makes a decision based on the ARTag's angle position.

        :param direction: The ARTag's direction.
        :type direction: float

        :return: Which way the ARTag is turning. -1 means left, 0 means
                 straight, and 1 means right.
        :rtype: int
        """
        if self._DEADZONE_LEFT < direction < 0:
            decision = -1
        elif 0 < direction < self._DEADZONE_RIGHT:
            decision = 1
        else:
            decision = 0

        return decision


    def detect(self, img_src=None):
        """
        Detect an ARTag.

        :param img_src: Path to an image. Used to bypass the camera feed and
                        track ARTags from images instead. Used primarily for
                        testing purposes. Disabled by default.
        :type img_src: str

        :return: Dictionary containing the x distance, z distance, direction,
                 decision, and yaw if an ARTag is detected.
        :rtype: float, float, float, int, float

        :return: None if a camera does not recognize an ARTag.
        :rtype: None

        :raise IOError: Thrown if img_src contains an invalid path.
        """
        if not img_src:
            self._ret, self._frame = self._cap.read()
        else:
            file_exists = os.path.isfile(img_src)
            if file_exists:
                self._frame = cv2.imread(img_src)
                self._frame = cv2.resize(self._frame,
                        (self.RESOLUTIONS[self._RESOLUTION][0],
                         self.RESOLUTIONS[self._RESOLUTION][1]))
            else:
                raise IOError('File does not exist')

        self._picture = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)

        self._picture = cv2.addWeighted(self._picture, self._CONTRAST,
                self._picture, 0, self._BRIGHTNESS)

        self._corners, ids, rejected_img_points = ar.detectMarkers(
            self._picture, self._AR_DICT, parameters=self._PARAMETERS)

        # If no corners found, return an empty object.
        if len(self._corners) == 0:
            return None

        rvec, tvec, _ = ar.estimatePoseSingleMarkers(self._corners[0],
                                                     self._MARKER_LENGTH,
                                                     self._CAMERA_MATRIX,
                                                     self._DIST_COEFFS)

        object_x = tvec[0][0][0]
        object_z = tvec[0][0][2]
        direction = self.get_direction(object_x, object_z)

        decision = self.make_decision(direction)

        # Get the rotation matrix of the tag. This will help find the yaw angle.
        rotation_matrix = np.zeros(shape=(3,3))
        cv2.Rodrigues(rvec[0][0], rotation_matrix, jacobian=0)

        # Decompose the rotation matrix into three rotation matrices for pitch,
        # yaw, and roll.
        pyr = cv2.RQDecomp3x3(rotation_matrix)

        # The rotation matrix of the yaw is as follows:
        # [cos(th)  0 sin(th)]
        # [   0     1    0   ]
        # [-sin(th) 0 cos(th)]
        #
        # We take the first cos result and feed it into the arccos function to
        # get the yaw angle.
        yaw_matrix = pyr[4]
        yaw_angle = np.arccos(yaw_matrix[0][0])
        yaw_angle = np.degrees(yaw_angle)

        self._tag_data['x'] = object_x
        self._tag_data['z'] = object_z
        self._tag_data['direction'] = direction
        self._tag_data['decision'] = decision
        self._tag_data['yaw'] = yaw_angle

        return self._tag_data


def main():
    """
    Displays ARTag information.

    Creates a TagRecognition object and prints tag information to the console.
    """
    tag = TagRecognition(contrast=2)

    while True:
        print(tag.detect())


if __name__ == '__main__':
    main()

