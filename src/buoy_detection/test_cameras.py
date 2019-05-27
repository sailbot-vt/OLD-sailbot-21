import cv2
import numpy as np
import os
import glob
import time
from src.buoy_detection.Depth_Map_Calculator import Depth_Map
from src.buoy_detection.Distance_Calculator import DistanceCalculator

CHESSBOARD_CALIBRATION_SIZE = (6, 8)
TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30,0.001)

def test():
    left = cv2.VideoCapture(2)
    right = cv2.VideoCapture(3)
    while(True):

        # Grab first in order to reduce asynchronous issues and latency
        if not left.grab() or not right.grab():
            print("Frames not grabbed")
            break

        read, left_frame = left.retrieve()
        read, right_frame = right.retrieve()

        cv2.imshow('left', left_frame)
        cv2.imshow('right', right_frame)

        if cv2.waitKey(33) == 27:
            break

    left.release()
    right.release()

def testFindCheckerboard():
    path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
    left_camera_directory = path + "LEFT"
    left_images = glob.glob("{0}/*.png".format(left_camera_directory))
    for image_path in sorted(left_images):
        print(image_path)
        image = cv2.imread(image_path)
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        has_corners, corners = cv2.findChessboardCorners(image_grey, CHESSBOARD_CALIBRATION_SIZE, cv2.CALIB_CB_FAST_CHECK)

        if has_corners:
            cv2.cornerSubPix(image_grey, corners, (11, 11), (-1, -1), TERMINATION_CRITERIA)
            cv2.drawChessboardCorners(image, CHESSBOARD_CALIBRATION_SIZE, corners, has_corners)
            cv2.imshow(left_camera_directory, image)
            #time.sleep(.2)


def testFindBuoyPixels():
    dist_calc = DistanceCalculator()
    while True:

        if cv2.waitKey(33) == 27:
            break

        # Closing is the opposite. It dilates and then erodes in order to fill in missing detections within detected images.
        kernel_close = np.ones((2, 2))
        kernel_open = np.ones((12,12))
        frame, disparity = dist_calc.depth_map_calculator.calculateDepthMap()
        frame_copy = frame
        disparity_copy = disparity

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        RED_ORANGE_LOW = np.array([10,100, 20],np.uint8)
        RED_ORANGE_HIGH = np.array([25,255,555],np.uint8)

        #mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
        mask = cv2.inRange(hsv, (10, 100, 20), (15,255,255))
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask = mask_open
        mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
        mask = mask_close

        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            cv2.drawContours(frame_copy, contours, -1, (0, 255, 0), 3)
            biggest = sorted(contours, key=cv2.contourArea)[-1]
            x, y, w, h = cv2.boundingRect(biggest)
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(disparity_copy, (x,y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("frameee", frame_copy)
        cv2.imshow("disparity", disparity_copy)


        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if len(contours) >= 1:
            # How to get center of object using moments:
            # https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
            contour = sorted(contours, key=cv2.contourArea)[-1]
            moment = cv2.moments(contour)
            center = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00']))

        else:
            print("No Moments found")

def testDisparityMap():

    dc = DistanceCalculator(DRAW_IMAGE= False, camera_numbers=(3,2))

    while True:
        left, depth_map = dc.depth_map_calculator.calculateDepthMap()
        cv2.imshow("leftss", left)
        cv2.imshow("disparity", depth_map)

def getCameraNumbers():
    cams = []
    cams_test = 10
    for i in range(0, cams_test):
        cap = cv2.VideoCapture(i)
        test, frame = cap.read()
        if test:
            cams.append(i)
    print(cams)

testDisparityMap()