# This script is used to generate a new AR tag
# Author: Wisam Bunni
import numpy as np
import cv2
import cv2.aruco as ar


def generate_blob():
    ar_dict = ar.Dictionary_get(ar.DICT_6X6_250)

    img = ar.drawMarker(ar_dict, 2, 700)
    cv2.imwrite('test_marker.jpg', img)

    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    generate_blob()


if __name__ == '__main__':
    main()
