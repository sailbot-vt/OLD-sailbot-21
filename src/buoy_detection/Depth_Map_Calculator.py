import numpy as np
import cv2
import os
from math import sqrt

# Focal length is 56 at red dot and 75 at blue dot
# Baseline should be in meters
default_calibration_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "stereo_calibration.npz"


class DepthMap:
    def __init__(self, calibration_path=default_calibration_path, fov=56, baseline=.2, camera_numbers=(2, 3),
                 draw_image=False):
        self.calibration = None

        try:
            self.calibration = np.load(calibration_path, allow_pickle=False)
        except IOError:
            print("Depth_Map Object could not load calibration data from the following location:")
            print(calibration_path)
        except ValueError:
            print("The calibration data at " + calibration_path +
                  " contains an object array but allow_pickle=False was given" +
                  "to the load function.")

        self.camera_numbers = camera_numbers
        self.image_size = tuple(self.calibration["image_size"])

        self.left_xmap = self.calibration["left_xmap"]
        self.left_ymap = self.calibration["left_ymap"]
        self.left_roi = tuple(self.calibration["left_roi"])

        self.right_xmap = self.calibration["right_xmap"]
        self.right_ymap = self.calibration["right_ymap"]
        self.right_roi = tuple(self.calibration["right_roi"])

        # TODO: Explain what this is
        self.pixel_degrees = 45 / sqrt((self.image_size[0] ^ 2 + self.image_size[1] ^ 2))
        self.FOV_RADS = np.deg2rad(fov)
        self.focal_length = self.calibration["Q_matrix"][0][0]
        self.baseline = baseline

        # The left and right camera objects, respectively.
        self.left = cv2.VideoCapture(camera_numbers[0])
        self.right = cv2.VideoCapture(camera_numbers[1])

        # TODO: Explain what things are drawn
        self.DRAW_IMAGE = draw_image

        #
        self.bm = cv2.StereoBM_create()
        self.bm.setMinDisparity(0)
        self.bm.setNumDisparities(160)
        self.bm.setBlockSize(5)
        self.bm.setROI1(self.left_roi)
        self.bm.setROI2(self.right_roi)
        self.bm.setUniquenessRatio(15)
        self.bm.setSpeckleWindowSize(0)
        self.bm.setSpeckleRange(2)
        self.REMAP_INTERPOLATION = cv2.INTER_LINEAR
        self.DEPTH_VISUALIZATION_SCALE = 32

    def calculateDepthMap(self):
        """
        Calculates the disparity map of a frame of the two cameras. This is used to get the distance of any given pixels

        :return:
        The left frame (original frame that is the same orientation as disparity) and the disparity map
        """
        # Grab first in order to reduce asynchronous issues and latency
        if not self.left.grab() or not self.right.grab():
            print("Frames not grabbed")
            return

        ### THIS HAS TO BE IN FOR THE FRAME RETRIEVAL TO WORK
        # DON'T REMOVE THIS
        if cv2.waitKey(33) == 27:
            return

        fixed_left = self.getLeftCameraImage()
        fixed_right = self.getRightCameraImage()
        grey_left = cv2.cvtColor(fixed_left, cv2.COLOR_BGR2GRAY)
        grey_right = cv2.cvtColor(fixed_right, cv2.COLOR_BGR2GRAY)
        depth = self.bm.compute(grey_left, grey_right)
        depth = depth.astype(np.uint8)
        if self.DRAW_IMAGE:
            cv2.imshow('left', grey_left)
            cv2.imshow('right', grey_right)
            cv2.imshow('depth', depth)
        return fixed_left, depth

    def getLeftCameraImage(self):
        """
        Gets a single frame of the left camera
        :return: a remapped frame from the camera
        """
        if not self.left.grab():
            print("Could not grab left camera image")
            return None

        # DON'T REMOVE THIS
        if cv2.waitKey(33) == 27:
            return
        read, left_frame = self.left.retrieve()
        fixed_left = cv2.remap(left_frame, self.left_xmap, self.left_ymap, self.REMAP_INTERPOLATION)
        return fixed_left

    def getRightCameraImage(self):
        """
        Gets a single frame of the right camera
        :return: a remapped frame from the camera
        """
        if not self.right.grab():
            print("Could not grab right camera image")
            return None

        # DON'T REMOVE THIS
        if cv2.waitKey(33) == 27:
            return
        read, right_frame = self.right.retrieve()
        fixed_left = cv2.remap(right_frame, self.right_xmap, self.right_ymap, self.REMAP_INTERPOLATION)
        return fixed_left
