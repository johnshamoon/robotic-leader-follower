# This script is used to detect an AR tag through Webcam in real time.
# It displays two plots:
# One to visualize the corners of the tag.
# One to visualize the pose of the tag (pitch, yaw, roll).
# Author: Wisam Bunni
import numpy as np
import cv2
import cv2.aruco as ar
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


RESOLUTIONS = {
        1080: [1920, 1080],
        720: [1280, 720],
        480: [720, 480],
        360: [480, 360],
        240: [426, 240],
        180: [320, 180],
        90: [160, 90]
}


def detect():

    # MATPLOTLIB
    ###
    style.use('fivethirtyeight')
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 2, 1, aspect='equal', adjustable='box')
    ax1.set_title('Corner Points')
    ax2 = fig.add_subplot(1, 2, 2, aspect='equal', adjustable='box')
    ax2.set_title('Tag Pose')
    ax2.legend(loc='upper right')
    ###

    RESOLUTION = 480 # Use to set the resolution for video feed

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTIONS[RESOLUTION][0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTIONS[RESOLUTION][1])

    corners = np.array([[0, 0]] * 4)

    marker_length = 0.06
    marker_size = 0.01

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

        picture = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        corners, ids, rejected_img_points = ar.detectMarkers(
            picture, ar_dict, parameters=parameters)

        picture = ar.drawDetectedMarkers(picture, corners)

        # A tag is detected
        if len(corners) == 0:
            continue

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

        picture = ar.drawAxis(picture, camera_matrix,
                              dist_coeffs, rvec, tvec, marker_size)

        # MATPLOTLIB
        ###
        for corner in corners[0]:
            for c in corner:
                ax1.scatter(c[0], c[1])

        ax2.scatter(rvec[0][0][0], rvec[0][0][0],
                    color='red', label='pitch')
        ax2.scatter(rvec[0][0][1], rvec[0][0][1],
                    color='blue', label='roll')
        ax2.scatter(rvec[0][0][2], rvec[0][0][2],
                    color='green', label='yaw')

        fig.canvas.draw()
        ax1.set_title('Tag Corners')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax2.set_title('Tag Pose')
        ax2.legend(loc='lower right', fontsize='x-small')
        plt.pause(0.001)
        fig.show()
        ax1.clear()
        ax2.clear()
        fig.canvas.flush_events()
        ###

        cv2.imshow('frame', picture)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == '__main__':
    detect()
