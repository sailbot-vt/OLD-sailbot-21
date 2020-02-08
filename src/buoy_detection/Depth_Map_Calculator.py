import numpy as np
import cv2
from math import sqrt


class DepthMap:
    def __init__(self, master_config):
        """Initialize the DepthMap.

        Inputs:
            master_config -- A loaded master YAML buoy_detection configuration object, loaded using config_reader.
        """

        config = master_config["depth_map"]

        # Load in variables from depth_map configuration.
        calibration_filename = config["calibration_filename"]
        hfov = config["hfov"]

        # Import calibration data.
        self.calibration = None
        try:
            self.calibration = np.load(calibration_filename, allow_pickle=False)
        except IOError:
            print("Depth_Map Object could not load calibration data from the following location:")
            print(calibration_filename)
        except ValueError:
            print("The calibration data at " + calibration_filename +
                  " contains an object array but allow_pickle=False was given" +
                  "to the load function.")

        self.camera_numbers = config["camera_numbers"]
        self.image_size = tuple(self.calibration["image_size"])

        self.left_xmap = self.calibration["left_xmap"]
        self.left_ymap = self.calibration["left_ymap"]
        self.left_roi = tuple(self.calibration["left_roi"])

        self.right_xmap = self.calibration["right_xmap"]
        self.right_ymap = self.calibration["right_ymap"]
        self.right_roi = tuple(self.calibration["right_roi"])

        self.hfov_rads = np.deg2rad(hfov)
        self.focal_length = self.calibration["Q_matrix"][0][0]
        self.baseline = master_config["common"]["baseline"]

        # The left and right camera objects, respectively.
        self.left = cv2.VideoCapture(self.camera_numbers[0])
        self.right = cv2.VideoCapture(self.camera_numbers[1])

        self.draw_image = config["draw_image"]

        # Creates the Stereo Block Matcher, which is used to find correspondences between the two stereo images
        # (i.e., which pair of image points [one from each image] refer to the same object point?)
        stereo_conf = config["stereo_bm"]

        self.bm = cv2.StereoBM_create()
        self.bm.setMinDisparity(stereo_conf["min_disparity"])
        self.bm.setNumDisparities(stereo_conf["num_disparities"])
        self.bm.setBlockSize(stereo_conf["block_size"])
        self.bm.setROI1(self.left_roi)
        self.bm.setROI2(self.right_roi)
        self.bm.setUniquenessRatio(stereo_conf["uniqueness_ratio"])
        self.bm.setSpeckleWindowSize(stereo_conf["speckle_window_size"])
        self.bm.setSpeckleRange(stereo_conf["speckle_range"])
        self.remap_interpolation = eval(stereo_conf["remap_interpolation"])
        self.depth_visualization_scale = stereo_conf["depth_visualization_scale"]

    def calculate_depth_map(self):
        """Calculates the disparity map of a frame of the two cameras.
        This is used to get the distance of any given pixels.

        Returns:
            The left frame (original frame in the same orientation as disparity) and the disparity map.
            If an error occurs, return (None, None).
        """
        # Grab first in order to reduce asynchronous issues and latency.
        if not self.left.grab() or not self.right.grab():
            print("Couldn't grab frames!")
            return None, None

        # This must be here for frame retrieval to work. Do not remove.
        # TODO: Find out why!!
        if cv2.waitKey(33) == 27:
            return None, None

        fixed_left = self.get_left_camera_image()
        fixed_right = self.get_right_camera_image()
        grey_left = cv2.cvtColor(fixed_left, cv2.COLOR_BGR2GRAY)
        grey_right = cv2.cvtColor(fixed_right, cv2.COLOR_BGR2GRAY)
        depth = self.bm.compute(grey_left, grey_right)
        depth = depth.astype(np.uint8)
        if self.draw_image:
            cv2.imshow('left', grey_left)
            cv2.imshow('right', grey_right)
            cv2.imshow('depth', depth)
        return fixed_left, depth

    def get_left_camera_image(self):
        """
        Gets a single frame of the left camera.

        Returns:
            A remapped frame from the camera, or None if an error occurs.
        """
        if not self.left.grab():
            print("Couldn't grab left camera frame!")
            return None

        # This must be here for frame retrieval to work. Do not remove.
        # TODO: Find out why!!
        if cv2.waitKey(33) == 27:
            return None
        read, left_frame = self.left.retrieve()
        fixed_left = cv2.remap(left_frame, self.left_xmap, self.left_ymap, self.remap_interpolation)
        return fixed_left

    def get_right_camera_image(self):
        """
        Gets a single frame of the right camera.

        Returns:
            A remapped frame from the camera, or
            None if an error occurs.
        """
        if not self.right.grab():
            print("Couldn't grab right camera frame!")
            return None

        # This must be here for frame retrieval to work. Do not remove.
        # TODO: Find out why!!
        if cv2.waitKey(33) == 27:
            return None
        read, right_frame = self.right.retrieve()
        fixed_left = cv2.remap(right_frame, self.right_xmap, self.right_ymap, self.remap_interpolation)
        return fixed_left
