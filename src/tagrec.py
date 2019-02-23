import numpy as np 
import cv2
import cv2.aruco as ar 


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
        self.__RESOLUTION = resolution
        self.__MARKER_LENGTH = marker_length
        self.__DEADZONE_RIGHT = dead_zone
        self.__DEADZONE_LEFT = -dead_zone
        
        self.__cap = cv2.VideoCapture(0)

        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.RESOLUTIONS[self.__RESOLUTION][0])
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.RESOLUTIONS[self.__RESOLUTION][1])

        self.__corners = np.array([[0,0]] * 4)

        self.__AR_DICT = ar.Dictionary_get(ar.DICT_6X6_250)
        self.__PARAMETERS = ar.DetectorParameters_create()

        self.__CALIBRATION_FILE = 'calibration.xml'
        self.__CALIBRATION_PARAMS = cv2.FileStorage(self.__CALIBRATION_FILE,
            cv2.FILE_STORAGE_READ)

        self.__DIST_COEFFS = self.__CALIBRATION_PARAMS.getNode('distCoeffs').mat()

        self.__ret, self.__frame = self.__cap.read()
        self.__size = self.__frame.shape 

        self.__FOCAL_LENGTH = self.__size[1]
        self.__CENTER = (self.__size[1]/2, self.__size[0]/2)

        self.__CAMERA_MATRIX = np.array(
            [[self.__FOCAL_LENGTH, 0, self.__CENTER[0]],
             [0, self.__FOCAL_LENGTH, self.__CENTER[1]],
             [0, 0, 1]], dtype='double'

        )

        self.__tag_data = {
                'x': 0,
                'z': 0,
                'direction': 0,
                'decision': 0
        }


    def get_direction(self, object_x, object_z):
        turn_angle = np.arctan(object_z / object_x)

        return turn_angle


    def make_decision(self, direction):
        if self.__DEADZONE_LEFT < direction < 0:
            decision = -1
        elif 0 < direction < self.__DEADZONE_RIGHT:
            decision = 1
        else:
            decision = 0

        return decision 
    

    def detect(self):
        self.__ret, self.__frame = self.__cap.read()
        
        self.__picture = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2GRAY)

        self.__corners, ids, rejected_img_points = ar.detectMarkers(
            self.__picture, self.__AR_DICT, parameters=self.__PARAMETERS)

        if len(self.__corners) == 0:
            return None

        rvec, tvec, _ = ar.estimatePoseSingleMarkers(self.__corners[0], self.__MARKER_LENGTH,
            self.__CAMERA_MATRIX, self.__DIST_COEFFS)

        object_x = tvec[0][0][0]
        object_z = tvec[0][0][2]
        direction = self.get_direction(object_x, object_z)

        decision = self.make_decision(direction)

        self.__tag_data['x'] = object_x
        self.__tag_data['z'] = object_z
        self.__tag_data['direction'] = direction
        self.__tag_data['decision'] = decision

        return self.__tag_data

