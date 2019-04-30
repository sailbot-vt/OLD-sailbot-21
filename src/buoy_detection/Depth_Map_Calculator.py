import numpy as np
import cv2
import os

# Focal length is 56 at red dot and 75 at blue dot
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "stereo_calibration.npz"
class Depth_Map():
    def __init__(self, calibration_directory = path, FOV = 56, baseline = .2, DRAW_IMAGE = False):
        self.calibration = None
        try:
            self.calibration = np.load(self.calibration_directory, allow_pickle=False)
            self.image_size = tuple(self.calibration["image_size"])
            self.left_xmap = self.calibration["left_xmap"]
            self.left_ymap = self.calibration["left_ymap"]
            self.left_roi = tuple(self.calibration["left_roi"])
            self.right_xmap = self.calibration["right_xmap"]
            self.right_ymap = self.calibration["right_ymap"]
            self.right_roi = tuple(self.calibration["right_roi"])
            self.pixel_degrees = 45/(self.image_size[0]^2 + self.image_size[1]^2)^1/2
            self.FOV_RADS = np.deg2rad(56)
            self.focal_length = self.calibration["Q_matrix"][0][0]
            self.baseline = baseline
        except:
            print("Depth_Map Object could not load calibration data in given location")

        try:
            self.left = cv2.VideoCapture(0)
            self.right = cv2.VideoCapture(1)
        except:
            print("Could not get feed from cameras")

        self.DRAW_IMAGE = DRAW_IMAGE
        self.stereoMatcher = cv2.StereoBM_create()
        self.stereoMatcher.setMinDisparity(4)
        self.stereoMatcher.setNumDisparities(128)
        self.stereoMatcher.setBlockSize(21)
        self.stereoMatcher.setROI1(self.left_roi)
        self.stereoMatcher.setROI2(self.right_roi)
        self.stereoMatcher.setSpeckleRange(16)
        self.stereoMatcher.setSpeckleWindowSize(45)
        self.REMAP_INTERPOLATION = cv2.INTER_LINEAR
        self.DEPTH_VISUALIZATION_SCALE = 128



    def calculateDepthMap(self):
        """
        Calculates the disparity map of a frame of the two cameras. This is used to get the distance of any given pixels

        :return:
        the disparity map
        """
        if not self.left.grab() or not self.right.grab():
            print("Frames not grabbed")
            return None
        read, left_frame = self.left.retrieve()
        read, right_frame = self.right.retrieve()

        fixed_left = cv2.remap(left_frame, self.left_xmap, self.left_ymap, self.REMAP_INTERPOLATION)
        fixed_right = cv2.remap(right_frame, self.right_xmap, self.right_ymap, self.REMAP_INTERPOLATION)

        grey_left = cv2.cvtColor(fixed_left, cv2.COLOR_BGR2GRAY)
        grey_right = cv2.cvtColor(fixed_right, cv2.COLOR_BGR2GRAY)
        depth = self.stereoMatcher.compute(grey_left, grey_right)
        depth = depth.astype(np.uint8)
        if self.DRAW_IMAGE:
            cv2.imshow('left', grey_left)
            cv2.imshow('right', grey_right)
            cv2.imshow('depth', depth)
        self.left.release()
        self.right.release()
        return depth


    def getLeftCameraImage(self):
        """
        Gets a single frame of the left camera
        :return: a remapped frame from the camera
        """
        if not self.left.grab():
            print("Could not grab left camera image")
            return None
        read, left_frame = self.left.retrieve()
        fixed_left = cv2.remap(left_frame, self.left_xmap, self.left_ymap, self.REMAP_INTERPOLATION)
        return fixed_left

    def getRightCameraImage(self):
        """
        Gets a single frame of the right camera
        :return: a remapped frame from the camera
        """
        if not self.right.grab():
            print("Could not grab left camera image")
            return None
        read, right_frame = self.right.retrieve()
        fixed_left = cv2.remap(right_frame, self.right_xmap, self.right_ymap, self.REMAP_INTERPOLATION)
        return fixed_left
