import cv2
from matplotlib import pyplot as plt
import numpy as np
import time

def generate_disparity_map(directory):

    directory = r'C:\Users\Wylans xps 13\PycharmProjects\SailBOT19\src\buoy_detection\x.npz'
    cal = np.load(directory, allow_pickle= False)
    print(cal.files)
    left_xmap = cal['arr_2']
    print(left_xmap)
    left_ymap = cal['arr_3']
    print(left_ymap)
    right_xmap = cal['arr_5']
    print(right_xmap)
    right_ymap = cal['arr_6']
    print(right_ymap)
    cam = cv2.VideoCapture(0)
    (grabbed, left_img) = cam.read()
    left_img = left_img.astype(np.uint8)
    time.sleep(1)
    (grabbed, right_img) = cam.read()
    right_img = right_img.astype(np.uint8)

    left_rectified = cv2.remap(left_img, left_xmap, left_ymap, cv2.INTER_LINEAR)
    right_rectified = cv2.remap(right_img, right_xmap, right_ymap, cv2.INTER_LINEAR)
    gray_left = cv2.cvtColor(left_rectified, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_rectified, cv2.COLOR_BGR2GRAY)

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(gray_left, gray_right)
    disparity = disparity.astype(np.uint8)
    cv2.imshow('left(R)', gray_left)
    cv2.imshow('right(R)', gray_right)
    cv2.imshow('Disparity', disparity)
    cv2.waitKey()

    return disparity

def generate_unrectified_disparity_map():
    cam = cv2.VideoCapture(0)
    (grabbed, left_img) = cam.read()
    left_img = left_img.astype(np.uint8)
    time.sleep(1)
    (grabbed, right_img) = cam.read()
    right_img = right_img.astype(np.uint8)

    gray_left = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(gray_left, gray_right)
    disparity = disparity.astype(np.uint8)

    cv2.imshow('left(R)', gray_left)
    cv2.imshow('right(R)', gray_right)
    cv2.imshow('Disparity', disparity)
    cv2.waitKey()

    return disparity

generate_unrectified_disparity_map()