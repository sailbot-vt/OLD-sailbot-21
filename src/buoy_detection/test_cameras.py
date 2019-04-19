import cv2
import numpy as np


CHESSBOARD_CALIBRATION_SIZE = (6, 9)



def test():
    left = cv2.VideoCapture(0)
    right = cv2.VideoCapture(1)
    left.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    left.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    right.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    right.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
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



def testFindBuoyPixels():
    left = cv2.VideoCapture(1)
    #right = cv2.VideoCapture(2)
    while True:

        if cv2.waitKey(33) == 27:
            break

        # Closing is the opposite. It dilates and then erodes in order to fill in missing detections within detected images.
        kernel_close = np.ones((10, 10))


        read, frame = left.retrieve()



        # image mask
        if not read:
            print("not grabbed")
            return
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)


        RED_ORANGE_LOW = np.array([100, 100, 0])
        RED_ORANGE_HIGH = np.array([255, 230, 200])
        kernel_open = np.ones((6, 6))

        mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)
        mask = mask_close

        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            biggest = sorted(contours, key=cv2.contourArea)[-1]
            x, y, w, h = cv2.boundingRect(biggest)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("frameee", frame)

        RED_ORANGE_HIGH = np.array([210, 100, 0])
        RED_ORANGE_LOW = np.array([255, 200, 20])
        kernel_open = np.ones((6, 6))

        mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)
        mask = mask_close

        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if len(contours) >= 1:
            # How to get center of object using moments:
            # https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
            contour = sorted(contours, key=cv2.contourArea)[-1]
            moment = cv2.moments(contour)
            center = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00']))

        else:
            print("No Moments found")

testFindBuoyPixels()