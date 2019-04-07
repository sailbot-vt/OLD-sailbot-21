import glob
import os
import numpy as np
import cv2

left_camera_directory = "/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/LEFT"
right_camera_directory = "/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/RIGHT"
images = glob.glob("{0}/*.png".format(imageDirectory))
not_has_corners = []
CHESSBOARD_CALIBRATION_SIZE = (6, 9)

def pre_calibration_removal(imageDirectory):
    images = glob.glob("{0}/*.png".format(imageDirectory))

    for image_path in sorted(images):
        image = cv2.imread(image_path)
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        has_corners, corners = cv2.findChessboardCorners(image_grey, CHESSBOARD_CALIBRATION_SIZE, cv2.CALIB_CB_FAST_CHECK)

        if not has_corners:
            not_has_corners.append(image[-5:])

    for x in not_has_corners:
        try:
            os.remove("/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/LEFT/" + x)
        except:
            continue
        try:
            os.remove("/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/RIGHT/" + x)

