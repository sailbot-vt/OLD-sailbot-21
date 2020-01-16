"""
calibration.py
Contains a class, Calibrator, that can compute calibration data for two stereo cameras based on a set of
image pairs from each of them.

For information and background on the calibration process, see `calibration_readme.md`.
"""

import glob
import os
import numpy as np
import cv2
from time import sleep
import logging
import src.buoy_detection.config_reader as config_reader


class Calibrator:
    """ Class that contains machinery for doing stereo camera calibration!
    To run the calibration process and save the results, instantiate this class and then use the `run_calibration`
    method.
    """

    def __init__(self, config):
        """ Initializes the Calibrator using the given configuration.
        *** See config.yaml for descriptions on each parameter. ***

        Inputs:
            config -- A loaded YAML calibration configuration, loaded via config_reader.py (also in buoy_detection).
                      See `config_reader.get_calibration_config()`.
        """

        self.square_size = config["chessboard_specs"]["square_size"]
        self.grid_shape = config["chessboard_specs"]["grid_shape"]

        self.base_path = config["base_path"]

        tc_conf = config["term_criteria"]
        self.term_criteria = (tc_conf["term_flags"], tc_conf["max_iterations"], tc_conf["min_accuracy"])

        self.rectification_alpha = config["rectification_alpha"]
        self.draw_image = config["draw_image"]

        self.corner_flags = config["finding_corners"]["corner_flags"]

        base_path = config["base_path"]
        self.left_camera_directory = base_path + "LEFT"
        self.right_camera_directory = base_path + "RIGHT"

        self.csp_window_size = config["finding_corners"]["csp_window_size"]
        self.csp_zero_zone = config["finding_corners"]["csp_zero_zone"]

        # Set of unreadable image file-names, used so we can exclude a _pair_ of images from analysis if one is
        # invalid (i.e., we can't read the chessboard).
        self.unreadable_images = set()

        self.delete_unreadable_images = config["delete_unreadable_images"]

    def run_calibration(self, out_file1, out_file2):
        """ Master method that enumerates through images, detects chessboard calibration pattern,
        and conducts calibration.
        Saves final result matrices to out_file1 and out_file2.

        Inputs:
            out_file1 -- The path to save the stereo calibration matrices.
            out_file2 -- The path to save the projection & rectification matrices.

        Side Effects:
            Calls self._remove_unreadable_image_pairs() to delete invalid calibration image pairs.
            Saves calibration data to out_file1 and out_file2 as described above.
        """

        left_image_points, right_image_points, camera_size = self._find_chessboards()

        # We need a list of object point lists, where each object point list corresponds to an image (in exactly
        # the same way that `left_image_points` and `right_image_points` are set up.
        # Since each image is *defined* to have the same set of object points, we just make a list here with as many
        # duplicate object point lists as we have images.
        object_points = [self._get_object_points()] * len(left_image_points)

        if self.delete_unreadable_images:
            self._remove_unreadable_image_pairs()

        self._calculate_calibration_matrices(object_points, left_image_points, right_image_points, camera_size,
                                             out_file1, out_file2)

    def _get_object_points(self):
        """ Calculates a numpy array of 3D object points that represent the internal corners of a chessboard.
        The 3D object points are written in the chessboard coordinate system (see above documentation).
        All corners are located at non-negative integer points on the XY-plane multiplied by the square_size.
        For example, if the following represents a grid of chessboard intersections:
            -----------> X-axis
          | A   B   C
          | D   E   F
          | G   H   I
          V
          Y-axis
        Then the positions of each intersection are given by:
        A = [0, 0, 0];                 B = [square_size, 0, 0];              C = [square_size*2, 0, 0];
        D = [0, square_size, 0];       E = [square_size, square_size, 0];    F = [square_size*2, square_size, 0];
        ... etc.

        Returns:
            A numpy array of 3D object points representing the internal corners of the chessboard, of shape
                 (self.grid_shape[0] * self.grid_shape[1], 3). Appears like [[0, 0, 0], [square_size, 0, 0], ... ].
        """

        # Create the list of object points, where each object point is zeroed to [0, 0, 0].
        object_points = np.zeros((self.grid_shape[0] * self.grid_shape[1], 3), np.float32)

        # Calculate the individual X & Y coordinates of each object point.
        # Effectively, this just creates a list of all non-negative integer object points (with Z=0) to represent each
        # corner, all multiplied by the square_size to scale it to real-world size.
        object_points[:, :2] = np.mgrid[0:self.grid_shape[0], 0:self.grid_shape[1]].T.reshape(-1, 2) * self.square_size

        return object_points

    def _find_chessboards(self):
        """ Calculates the object points and image points of chessboard images.
        REQUIRES that the `left_camera_directory` and `right_camera_directory` have corresponding image pairs
        (and _only_ corresponding image pairs!).

        Returns:
            A 3-tuple with the list of left image points, the list of right image points, and the camera size.

        Side Effects:
            Updates the self.unreadable_images set.
            Draws images with detected corners overlaid if self.draw_image == True.
        """
        print("Reading images at {0}".format(self.left_camera_directory))
        left_image_paths = glob.glob("{0}/*.png".format(self.left_camera_directory))
        image_names = [os.path.basename(path) for path in left_image_paths]

        # A list of object point arrays and image point arrays across all of the analyzed images.
        image_points_l = []
        image_points_r = []
        camera_size = None

        for image_name in sorted(image_names):
            left_path = self.left_camera_directory + "/" + image_name
            right_path = self.right_camera_directory + "/" + image_name

            left_image = cv2.imread(left_path)
            left_grey = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)

            right_image = cv2.imread(right_path)
            right_grey = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

            camera_size = left_image.shape[::-1]

            has_corners_l, corners_l = cv2.findChessboardCorners(left_grey, self.grid_shape, self.corner_flags)

            has_corners_r, corners_r = cv2.findChessboardCorners(right_grey, self.grid_shape, self.corner_flags)

            if has_corners_l and has_corners_r:
                # Refine corner image points.
                cv2.cornerSubPix(left_grey, corners_l, self.csp_window_size, self.csp_zero_zone, self.term_criteria)
                cv2.cornerSubPix(right_grey, corners_r, self.csp_window_size, self.csp_zero_zone, self.term_criteria)
                image_points_l.append(corners_l)
                image_points_r.append(corners_r)
            else:
                if not has_corners_l:
                    self._find_corners_fail(left_path)

                if not has_corners_r:
                    self._find_corners_fail(right_path)

            if self.draw_image:
                cv2.drawChessboardCorners(left_image, self.grid_shape, corners_l, has_corners_l)
                cv2.drawChessboardCorners(right_image, self.grid_shape, corners_r, has_corners_r)
                cv2.imshow(left_path, left_image)
                cv2.imshow(right_path, right_image)
                sleep(.1)
                cv2.waitKey(1)

        print("Found corners in {0} out of {1} images".format(len(image_points_l), len(image_names)))

        return image_points_l, image_points_r, camera_size

    def _find_corners_fail(self, path):
        """ Handler for when an invalid image (illegible chessboard corners, etc.) is found.

        Inputs:
            path -- The path to the invalid image.

        Side Effects:
            Adds the image's basename to `self.unreadable_images`.
        """
        print("Corners could not be found in " + path + "!")
        name = os.path.basename(path)
        self.unreadable_images.add(name)

    def _remove_unreadable_image_pairs(self):
        """ Removes unreadable image pairs.

        Side Effects:
            Removes images from the left and right camera directories that are part of a pair in which at least one
            image has been marked as unreadable by `self.unreadable_images`.
        """
        for image_name in self.unreadable_images:
            left_image_path = self.left_camera_directory + "/" + image_name
            right_image_path = self.right_camera_directory + "/" + image_name

            try:
                os.remove(left_image_path)
            except:
                logging.getLogger().error("Failed to remove LEFT image " + left_image_path + "!", exc_info=True)

            try:
                os.remove(right_image_path)
            except:
                logging.getLogger().error("Failed to remove RIGHT image " + right_image_path + "!", exc_info=True)

    def _calculate_calibration_matrices(self, object_points, left_image_points, right_image_points, camera_size,
                                        calibration_filename, projection_filename):
        """ Actually conducts the camera calibration, and then saves the result.
        Do not run directly - instead, do `run_calibration`.

        Inputs:
            object_points -- A list of object point lists, describing which object points were found in which image.
                             Since all the images should contain the chessboard, and our 3D coordinate system is
                             standardized with respect to the chessboard, all the object point lists should be the
                             same (see `_get_object_points`).
            left_image_points -- A list of lists of 2D image points from the left camera. Should correspond to the
                                 points in `object_points` and `right_image_points`.
            right_image_points -- A list of lists of 2D image points from the right camera. Should correspond to the
                                  points in `object_points` and `left_image_points`.
            camera_size -- The resolution of the camera.
            calibration_filename -- The path to save the stereo calibration matrices.
            projection_filename -- The path to save the projection & rectification matrices.

        Side Effects:
            Saves calibration data to out_file1 and out_file2.
        """
        print("Calibrating left camera...")
        _, left_camera_matrix, left_distortion_coefficients, _, _ = \
            cv2.calibrateCamera(object_points, left_image_points, camera_size, None, None)
        print("Done")

        print("Calibrating right camera...")
        _, right_camera_matrix, right_distortion_coefficients, _, _ = \
            cv2.calibrateCamera(object_points, right_image_points, camera_size, None, None)
        print("Done")

        # rotationMatrix is the rotation between coordinate systems of the first and second cameras
        # translationVector is the translation between the coordinate systems of the two cameras
        print("Calibrating stereo cameras...")
        (_, _, _, _, _, rotationMatrix, translationVector, _, _) = \
            cv2.stereoCalibrate(
                object_points, left_image_points, right_image_points,
                left_camera_matrix, left_distortion_coefficients,
                right_camera_matrix, right_distortion_coefficients,
                camera_size, None, None, None, None,
                cv2.CALIB_FIX_INTRINSIC, self.term_criteria)
        print("Done")

        print("Starting stereo rectification...")
        # Rectification matrices are the 3x3 matrices that rotate them onto a common plane (so that their epipolar
        # lines are parallel and disparities only occur horizontally).
        #
        # Project matrices are the new rectified coordinate systems for each of the two cameras that map points
        # in 3D space to points in 2D image space.
        #
        # Q is the disparity to depth mapping in homogeneous coordinates - essentially allows you to
        # take the 2D coordinates of a pixel and its disparity, and find its 3D location.
        #   (input: 4-vector of the form [u, v, d, 1]
        #       where u, v are pixel coordinates and d is disparity;
        #   output: 4-vector of the form [x, y, z, w] where
        #       x, y, and z are 3D coordinates and w scales them appropriately (see 'Homogeneous coordinates')
        (leftRectification, rightRectification, left_projection, right_projection,
         Q_matrix, left_roi, right_roi) = \
            cv2.stereoRectify(
                left_camera_matrix, left_distortion_coefficients,
                right_camera_matrix, right_distortion_coefficients,
                camera_size, rotationMatrix, translationVector,
                None, None, None, None, None,
                cv2.CALIB_ZERO_DISPARITY, self.rectification_alpha)
        print("Done")

        # X and Y maps are the projection maps
        print("Saving the stereo calibration...")
        left_xmap, left_ymap = \
            cv2.initUndistortRectifyMap(
                left_camera_matrix, left_distortion_coefficients, leftRectification,
                left_projection, camera_size, cv2.CV_32FC1)
        right_xmap, right_ymap = \
            cv2.initUndistortRectifyMap(
                right_camera_matrix, right_distortion_coefficients, rightRectification,
                right_projection, camera_size, cv2.CV_32FC1)

        np.savez_compressed(calibration_filename, image_size=camera_size,
                            left_xmap=left_xmap, left_ymap=left_ymap, left_roi=left_roi,
                            right_xmap=right_xmap, right_ymap=right_ymap, right_roi=right_roi, Q_matrix=Q_matrix)

        np.savez_compressed(projection_filename, leftRectification=leftRectification,
                            rightRectification=rightRectification,
                            leftProjection=left_projection, rightProjection=right_projection,
                            Q_matrix=Q_matrix)
        cv2.destroyAllWindows()
        print("Done")


if __name__ == "__main__":
    CONFIG = config_reader.get_calibration_config()

    calibrator = Calibrator(CONFIG)

    calibration_export_filename = CONFIG["calibration_export_filename"]
    projection_export_filename = CONFIG["projection_export_filename"]

    calibrator.run_calibration(calibration_export_filename, projection_export_filename)
