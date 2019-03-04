import sys 
import numpy as np 
import cv2
import cv2.aruco as ar 


'''
Tag Recognition class.

Takes input from the camera to look for an ARTag.
Returns useful information about the tag.
'''
class TagRecognition():

    RESOLUTIONS = {
            1080: [1920, 1080],
            720: [1280, 720],
            480: [720, 480],
            360: [480, 360],
            240: [426, 240],
            180: [320, 180],
            90: [160, 90]
    }


    def __init__(self, resolution=90, dead_zone=1.45, marker_length=0.06):
        self._RESOLUTION = resolution
        self._MARKER_LENGTH = marker_length

        # Handle a special case
        # where the user requests to have no dead zones
        if dead_zone == 0:
            self._DEADZONE_RIGHT = sys.maxsize
            self._DEADZONE_LEFT = -sys.maxsize
        else:
            self._DEADZONE_RIGHT = abs(dead_zone)
            self._DEADZONE_LEFT = -self._DEADZONE_RIGHT
        
        self._cap = cv2.VideoCapture(0)

        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.RESOLUTIONS[self._RESOLUTION][0])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.RESOLUTIONS[self._RESOLUTION][1])

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

        # Set up a camera matrix 
        # This will allow to estimate the pose of the ARTag
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


    '''
    Gets the angle of the tag location 
    With respect to the camera.
    Input: Tag's X location and Z location.
    Output: Angle position.
    '''
    def get_direction(self, object_x, object_z):
        turn_angle = np.arctan(object_z / object_x)

        return turn_angle


    '''
    Makes a decision based on the tag's angle position.
    Input: Tag's direction.
    Output: Vehicle Decision.

    Signal definitions:
     -1: Turn left
     0: Go straight
     1: Turn right
    '''
    def make_decision(self, direction):
        if self._DEADZONE_LEFT < direction < 0:
            decision = -1
        elif 0 < direction < self._DEADZONE_RIGHT:
            decision = 1
        else:
            decision = 0

        return decision 
    

    '''
    Detect an AR Tag.
    Returns a dictionary with useful tag data.
    Returns None if camera doesn't recognize a tag.
    '''
    def detect(self):
        self._ret, self._frame = self._cap.read()
        
        self._picture = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)

        self._corners, ids, rejected_img_points = ar.detectMarkers(
            self._picture, self._AR_DICT, parameters=self._PARAMETERS)

        # If no corners found, return an empty object.
        if len(self._corners) == 0:
            return None

        rvec, tvec, _ = ar.estimatePoseSingleMarkers(self._corners[0], self._MARKER_LENGTH,
            self._CAMERA_MATRIX, self._DIST_COEFFS)

        object_x = tvec[0][0][0]
        object_z = tvec[0][0][2]
        direction = self.get_direction(object_x, object_z)

        decision = self.make_decision(direction)

        # Get the rotation matrix of the tag
        # This will help us find the yaw angle
        rotation_matrix = np.zeros(shape=(3,3))
        cv2.Rodrigues(rvec[0][0], rotation_matrix, jacobian=0)

        # Decompose the rotation matrix into three rotation matrices
        # For Pitch, Yaw, Roll 
        pyr = cv2.RQDecomp3x3(rotation_matrix)

        '''
        The rotation matrix of the yaw is as follows:
        [cos(th)  0 sin(th)]
        [   0     1    0   ]
        [-sin(th) 0 cos(th)]
        
        We take the first cos result and feed it into the arccos function
        to get the yaw angle.
        '''
        yaw_matrix = pyr[4]
        yaw_angle = np.arccos(yaw_matrix[0][0])
        yaw_angle = yaw_angle*(180/np.pi)

        self._tag_data['x'] = object_x
        self._tag_data['z'] = object_z
        self._tag_data['direction'] = direction
        self._tag_data['decision'] = decision
        self._tag_data['yaw'] = yaw_angle

        return self._tag_data

