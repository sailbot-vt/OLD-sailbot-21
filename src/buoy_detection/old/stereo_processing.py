import cv2
from matplotlib import pyplot as plt
import numpy as np
import time

CROP_WIDTH = 960
def cropHorizontal(image, CAMERA_WIDTH, CAMERA_HEIGHT):
    return image[:,
            int((CAMERA_WIDTH-100)/2):
            int(100+(CAMERA_WIDTH-100)/2)]

def generate_disparity_map(CAMERA_WIDTH,CAMERA_HEIGHT):
    directory = r'C:\Users\Wylans xps 13\PycharmProjects\SailBOT19\src\buoy_detection\x.npz'
    cal = np.load(directory, allow_pickle= False)
    left = cv2.VideoCapture(0)
    right = cv2.VideoCapture(1)

    #left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    #left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    #right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    #right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)


    stereoMatcher = cv2.StereoBM_create()
    #stereoMatcher.setMinDisparity(4)
    #stereoMatcher.setNumDisparities(1024 )
    #stereoMatcher.setBlockSize(21)
    #stereoMatcher.setROI1(tuple(cal['left_roi']))
    #stereoMatcher.setROI2(tuple(cal['right_roi']))
    #stereoMatcher.setSpeckleRange(16)
    #stereoMatcher.setSpeckleWindowSize(45)

    _, left_frame = left.read()
    #leftFrame = cropHorizontal(left_frame, CAMERA_WIDTH, CAMERA_HEIGHT)
    #leftHeight, leftWidth = leftFrame.shape[:2]
    _, right_frame = right.read()
    #rightFrame = cropHorizontal(right_frame, CAMERA_WIDTH, CAMERA_HEIGHT)
    #rightHeight, rightWidth = rightFrame.shape[:2]

    left_rectified = cv2.remap(left_frame, cal['left_xmap'], cal['left_ymap'], cv2.INTER_LINEAR)
    right_rectified = cv2.remap(right_frame, cal['right_xmap'], cal['right_ymap'], cv2.INTER_LINEAR)

    grey_left = cv2.cvtColor(left_rectified, cv2.COLOR_BGR2GRAY)
    grey_right = cv2.cvtColor(right_rectified, cv2.COLOR_BGR2GRAY)
    depth = stereoMatcher.compute(grey_left, grey_right)
    depth = depth.astype(np.uint8)
    cv2.imshow('left', grey_left)
    cv2.imshow('right', grey_right)
    cv2.imshow('depth', depth)
    cv2.waitKey()
    #return disparity

def generate_unrectified_disparity_map():
    cam = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(1)


    (grabbed, left_img) = cam.read()
    left_img = left_img.astype(np.uint8)
    time.sleep(1)
    (grabbed, right_img) = cam2.read()
    right_img = right_img.astype(np.uint8)

    gray_left = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

    stereo = cv2.StereoBM_create(numDisparities=128, blockSize=5)
    disparity = stereo.compute(gray_left, gray_right)
    disparity = disparity.astype(np.uint8)

    cv2.imshow('left(R)', gray_left)
    cv2.imshow('right(R)', gray_right)
    cv2.imshow('Disparity', disparity)
    cv2.waitKey()

    return disparity

def test():
    cam = cv2.VideoCapture(2)
    cam2 = cv2.VideoCapture(0)
    while (cv2.waitKey(33) != ord(" ")):
        (grabbed, frame) = cam.read()
        (grabbed2, frame2) = cam2.read()
        cv2.imshow("left", frame)
        cv2.imshow("right", frame2)
        if cv2.waitKey(33) == 27:
            cv2.release()
            cv2.destroyAllWindows()
            break
test()