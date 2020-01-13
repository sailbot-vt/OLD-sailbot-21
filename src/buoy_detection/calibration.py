import glob
import os
import numpy as np
import cv2
from time import sleep
import logging
import sys


class Calibrator:
    def __init__(self, square_size, grid_shape, base_path=None,
                 options=(cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK | cv2.CALIB_CB_ADAPTIVE_THRESH),
                 term_criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001),
                 optimize_alpha=0.25,
                 draw_image=True):
        """
        Class that contains machinery for doing stereo camera calibration!
        Requires a stereo set of images from a pair of LEFT/RIGHT cameras, which are each PARALLEL (extremely
        important!).
        Each image must contain a chessboard calibration pattern visible to BOTH cameras. The parameters of the
        chessboard pattern must be entered into this class through `square_size` and `grid_size` (see below).
        The images must be stored in `base_path/LEFT` and `base_path/RIGHT`, respectively.
        For accurate calibration, the chessboard pattern must be printed extremely accurately
        (laser-printer recommended).
        To run the calibration process and save the results, instantiate this class and then use the `run_calibration`
        method.
        :param square_size: The real size of each chessboard square, in meters.
        :param grid_shape: The shape of the grid of internal chessboard squares, as a 2-tuple of the form (x_size,
                           y_size).
        :param base_path: The path to the directory containing the LEFT/RIGHT camera image folders and where the
                          calibration matrices will be outputted. If None, defaults to the directory containing this
                          script.
        :param options: OpenCV2 option flags that specify how chessboard corners are found.
        :param term_criteria: Termination criteria for various iterative calibration processes (including corner
                              refinement [`cornerSubPix`] and stereo calibration).
        :param optimize_alpha: Alpha parameter for stereo rectification.
        :param draw_image: If True, displays each image as it is processed with the detected chessboard corners
                           overlaid.
        """

        self.square_size = square_size
        self.grid_shape = grid_shape

        self.base_path = base_path

        # Set the base_path to the directory of this script if no base_path is specified.
        if self.base_path is None:
            self.base_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]

        self.term_criteria = term_criteria
        self.optimize_alpha = optimize_alpha
        self.draw_image = draw_image

        self.options = options

        self.left_camera_directory = base_path + "LEFT"
        self.right_camera_directory = base_path + "RIGHT"

    def run_calibration(self, out_file1, out_file2):
        """
        Master method that enumerates through images, detects chessboard calibration pattern, and conducts calibration.
        Saves final result matrices to out_file1 and out_file2.
        :param out_file1: The path to save the stereo calibration matrices.
        :param out_file2: The path to save the projection & rectification matrices.
        TODO: Make these names/descriptions better.
        """

        (object_points, left_image_points, camera_size) = \
            self._find_chessboards(self.left_camera_directory)

        (_, right_image_points, _) = \
            self._find_chessboards(self.right_camera_directory)

        self._calculate_calibration_matrices(object_points, left_image_points, right_image_points, camera_size,
                                             out_file1, out_file2)

    def _get_object_points(self):
        """
        Calculates a numpy array of 3D object points that represent the internal corners of a chessboard.
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

        :return: A numpy array of 3D object points representing the internal corners of the chessboard, of shape
                 (self.grid_shape[0] * self.grid_shape[1], 3). Appears like [[0, 0, 0], [square_size, 0, 0], ... ].
        """

        # Create the list of object points, where each object point is zeroed to [0, 0, 0].
        object_points = np.zeros((self.grid_shape[0] * self.grid_shape[1], 3), np.float32)

        # Calculate the individual X & Y coordinates of each object point.
        # Effectively, this just creates a list of all non-negative integer object points (with Z=0) to represent each
        # corner, all multiplied by the square_size to scale it to real-world size.
        object_points[:, :2] = np.mgrid[0:self.grid_shape[0], 0:self.grid_shape[1]].T.reshape(-1, 2) * self.square_size

        return object_points

    def _find_chessboards(self, image_directory):
        """
        Calculates the object points and image points of chessboard images.
        :return: A 3-tuple with the object points list, the image points list, and resolution of the camera
        """
        print("Reading images at {0}".format(image_directory))
        images = glob.glob("{0}/*.png".format(image_directory))

        # The template list of object points.
        object_point_zero = self._get_object_points()

        # A list of object point arrays and image point arrays across all of the analyzed images.
        object_points = []
        image_points = []
        camera_size = None

        for image_path in sorted(images):
            image = cv2.imread(image_path)
            image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            camera_size = image_grey.shape[::-1]

            has_corners, corners = cv2.findChessboardCorners(image_grey, self.grid_shape,
                                                             self.options)

            if has_corners:
                object_points.append(object_point_zero)

                # Refine corner image points.
                cv2.cornerSubPix(image_grey, corners, (11, 11), (-1, -1), self.term_criteria)
                image_points.append(corners)
            else:
                print("Corners could not be found in " + image_path + "! Removing...")
                try:
                    os.remove(image_path)
                except:
                    logging.getLogger().error("Error deleting file " + image_path, exc_info=True)

            if self.draw_image:
                cv2.drawChessboardCorners(image, self.grid_shape, corners, has_corners)
                cv2.imshow(image_directory, image)
                sleep(.1)
                cv2.waitKey(1)

        print("Found corners in {0} out of {1} images".format(len(image_points), len(images)))

        return object_points, image_points, camera_size

    def _calculate_calibration_matrices(self, object_points, left_image_points, right_image_points, camera_size,
                                        out_file1, out_file2):
        """
        Actually conducts the camera calibration, and then saves the result.
        Do not run directly - instead, do `run_calibration`.
        :param object_points: A list of object point lists, describing which object points were found in which image.
                              Since all the images should contain the chessboard, and our 3D coordinate system is
                              standardized with respect to the chessboard, all the object point lists should be the
                              same (see `_get_object_points`).
        :param left_image_points: A list of lists of 2D image points from the left camera. Should correspond to the
                                  points in `object_points` and `right_image_points`.
        :param right_image_points: A list of lists of 2D image points from the right camera. Should correspond to the
                                   points in `object_points` and `left_image_points`.
        :param camera_size: The resolution of the camera.
        :param out_file1: The path to save the stereo calibration matrices.
        :param out_file2: The path to save the projection & rectification matrices.
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
        # Rectification matrices are the 3x3 rotation matrices for each of the two cameras
        # Project matrices are the new rectified coordinate systems for each of the two cameras
        # Q is the disparity to depth mapping
        (leftRectification, rightRectification, left_projection, right_projection,
         Q_matrix, left_roi, right_roi) = \
            cv2.stereoRectify(
                left_camera_matrix, left_distortion_coefficients,
                right_camera_matrix, right_distortion_coefficients,
                camera_size, rotationMatrix, translationVector,
                None, None, None, None, None,
                cv2.CALIB_ZERO_DISPARITY, self.optimize_alpha)
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

        np.savez_compressed(out_file1, image_size=camera_size,
                            left_xmap=left_xmap, left_ymap=left_ymap, left_roi=left_roi,
                            right_xmap=right_xmap, right_ymap=right_ymap, right_roi=right_roi, Q_matrix=Q_matrix)

        np.savez_compressed(out_file2, leftRectification=leftRectification, rightRectification=rightRectification,
                            leftProjection=left_projection, rightProjection=right_projection,
                            Q_matrix=Q_matrix)
        cv2.destroyAllWindows()
        print("Done")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Format: " + sys.argv[0] + " <base_path>")
        sys.exit(1)

    BASE_PATH = sys.argv[1]

    CHESSBOARD_SQUARE_SIZE = .024
    CHESSBOARD_GRID_SHAPE = (6, 9)

    OUT_FILE1 = BASE_PATH + "stereo_calibration.npz"
    OUT_FILE2 = BASE_PATH + "projection_matrices.npz"

    calibrator = Calibrator(CHESSBOARD_SQUARE_SIZE, CHESSBOARD_GRID_SHAPE, base_path=BASE_PATH,
                            options=cv2.CALIB_CB_FAST_CHECK)
    calibrator.run_calibration(OUT_FILE1, OUT_FILE2)
