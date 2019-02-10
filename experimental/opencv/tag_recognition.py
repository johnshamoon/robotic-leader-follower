# This script is used to detect an AR tag through Webcam in real time.
import numpy as np
import cv2
import cv2.aruco as ar

RESOLUTIONS = {
        1080: [1920, 1080],
        720: [1280, 720],
        480: [720, 480]
}


def detect():

    RESOLUTION = 480 # Use this to set the resolution for video feed

    cap = cv2.VideoCapture(0)

    corners = np.array([[0, 0]] * 4)

    marker_length = 0.25
    marker_size = 0.10

    ar_dict = ar.Dictionary_get(ar.DICT_6X6_250)
    parameters = ar.DetectorParameters_create()

    calibration_file = "calibration.xml"
    calibration_params = cv2.FileStorage(
        calibration_file, cv2.FILE_STORAGE_READ)

    camera_matrix = calibration_params.getNode("cameraMatrix").mat()
    dist_coeffs = calibration_params.getNode("distCoeffs").mat()

    while True:
        ret, frame = cap.read()

        size = frame.shape

        picture = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected_img_points = ar.detectMarkers(
            picture, ar_dict, parameters=parameters)

        # FOR MARKER DRAWING
        # UNCOMMENT TO SEE BORDER AROUND TAG IN CAMERA VIEW
        #picture = ar.drawDetectedMarkers(picture, corners)

        if len(corners) == 0:
            continue

        # A tag is detected
        print(corners[0])
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype='double'
        )

        # Get rotation and translation vectors
        rvec, tvec, _ = ar.estimatePoseSingleMarkers(
            corners[0], marker_length, camera_matrix, dist_coeffs)

        # FOR POSE DRAWING
        # UNCOMMENT TO SEE AXIS ON THE TAG IN CAMERA VIEW
        #picture = ar.drawAxis(picture, camera_matrix,
        #                      dist_coeffs, rvec, tvec, marker_size)

        # FOR CAMERA VIEW
        # UNCOMMENT TO SEE THE CAMERA FEED
        #cv2.imshow('frame', picture)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == '__main__':
    detect()
