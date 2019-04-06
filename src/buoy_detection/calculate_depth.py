import numpy as np
import cv2

REMAP_INTERPOLATION = cv2.INTER_LINEAR

DEPTH_VISUALIZATION_SCALE = 128

calibration = np.load("C:/Users/Wylans xps 13/PycharmProjects/SailBOT19/src/buoy_detection/camera_capture/stereo_calibration.npz", allow_pickle=False)

image_size = tuple(calibration["image_size"])
left_xmap = calibration["left_xmap"]
left_ymap = calibration["left_ymap"]
left_roi = tuple(calibration["left_roi"])
right_xmap = calibration["right_xmap"]
right_ymap = calibration["right_ymap"]
right_roi = tuple(calibration["right_roi"])
print("left_xmap")
print(left_xmap)
print("left_ymap")
print(left_ymap)
print("left_ROI")
print(left_roi)
print("right_xmap")
print(right_xmap)
print("right_ymap")
print(right_ymap)
print("right_ROI")
print(right_roi)

left = cv2.VideoCapture(0)
right = cv2.VideoCapture(2)

stereoMatcher = cv2.StereoBM_create()
stereoMatcher.setMinDisparity(4)
stereoMatcher.setNumDisparities(128)
stereoMatcher.setBlockSize(21)
stereoMatcher.setROI1(left_roi)
stereoMatcher.setROI2(right_roi)
stereoMatcher.setSpeckleRange(16)
stereoMatcher.setSpeckleWindowSize(45)

while(True):
    # Grab first in order to reduce asynchronous issues and latency
    if not left.grab() or not right.grab():
        print("Frames not grabbed")
        break

    read, left_frame = left.retrieve()
    read, right_frame = right.retrieve()

    fixed_left = cv2.remap(left_frame, left_xmap, left_ymap, REMAP_INTERPOLATION)
    fixed_right = cv2.remap(right_frame, right_xmap, right_ymap, REMAP_INTERPOLATION)

    grey_left = cv2.cvtColor(fixed_left, cv2.COLOR_BGR2GRAY)
    grey_right = cv2.cvtColor(fixed_right, cv2.COLOR_BGR2GRAY)
    depth = stereoMatcher.compute(grey_left, grey_right)

    cv2.imshow('left', grey_left)
    cv2.imshow('right', grey_right)
    depth = depth.astype(np.uint8)
    cv2.imshow('depth', depth)
    # Press escape to quit
    if cv2.waitKey(33) == 27:
        break

left.release()
right.release()
cv2.destroyAllWindows()