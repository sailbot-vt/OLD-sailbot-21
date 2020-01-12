import glob
import os
import numpy as np
import cv2
from time import sleep
import logging


# TODO: Write fleshed-out explanation for calibration process (including chessboard coordinate system)


def get_object_points(x_size, y_size, interval_size):
    """
    Calculates a numpy array of 3D object points that represent the internal corners of a chessboard.
    The 3D object points are written in the chessboard coordinate system (see above documentation).
    All corners are located at non-negative integer points on the XY-plane multiplied by the interval_size.
    For example, if the following represents a grid of chessboard intersections:
        -----------> X-axis
      | A   B   C
      | D   E   F
      | G   H   I
      V
      Y-axis
    Then the positions of each intersection are given by:
    A = [0, 0, 0];                 B = [interval_size, 0, 0];              C = [interval_size*2, 0, 0];
    D = [0, interval_size, 0];     E = [interval_size, interval_size, 0];  F = [interval_size*2, interval_size, 0];
    ... etc.

    :param x_size: The number of corners along the chessboard internal corner grid's X-dimension.
    :param y_size: The number of corners along the chessboard internal corner grid's Y-dimension.
    :param interval_size: The physical distance (in meters) between each corner (i.e., chessboard square size).
    :return: A numpy array of 3D object points representing the internal corners of the chessboard, of shape
             (x_size * y_size, 3). Appears like [[0, 0, 0], [interval_size, 0, 0], ... ].
    """

    # Create the list of object points, where each object point is zeroed to [0, 0, 0].
    object_points = np.zeros((x_size * y_size, 3), np.float32)

    # Calculate the individual X & Y coordinates of each object point.
    # Effectively, this just creates a list of all non-negative integer object points (with Z=0) to represent each
    # corner, all multiplied by the interval_size to scale it to real-world size.
    object_points[:, :2] = np.mgrid[0:x_size, 0:y_size].T.reshape(-1, 2) * interval_size

    return object_points


# File-names and directories
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
left_camera_directory = path + "LEFT"
right_camera_directory = path + "RIGHT"
out_file1 = path + "stereo_calibration.npz"
out_file2 = path + "projection_matrices.npz"


def find_chessboards(image_directory, grid_size, square_size, termination_criteria, draw_image):
    """
    Calculates the object points and image points of chessboard images
    :param image_directory: the directory to look through for chessboard images
    :param grid_size: The size of the chessboard's internal corner grid, as a 2-tuple of the form (x_size, y_size).
    :param square_size: The physical length of the chessboard's squares, in meters.
    :param termination_criteria: The OpenCV2 criteria for determining when to stop refining the corner image points
                                 (see `cv2.cornerSubPix`).
    :param draw_image: If True, display the images as they're analyzed with the detected corners highlighted.
    :return: A 3-tuple with the object points list, the image points list, and resolution of the camera
    """
    print("Reading images at {0}".format(image_directory))
    images = glob.glob("{0}/*.png".format(image_directory))

    # The template list of object points.
    object_point_zero = get_object_points(grid_size[0], grid_size[1], square_size)

    # A list of object point arrays and image point arrays across all of the analyzed images.
    object_points = []
    image_points = []
    camera_size = None

    for image_path in sorted(images):
        image = cv2.imread(image_path)
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        camera_size = image_grey.shape[::-1]

        has_corners, corners = cv2.findChessboardCorners(image_grey, grid_size,
                                                         cv2.CALIB_CB_FAST_CHECK)

        # TODO: Determine if we need the pre-image check if we can just check here
        if has_corners:
            object_points.append(object_point_zero)

            # Refine corner image points.
            cv2.cornerSubPix(image_grey, corners, (11, 11), (-1, -1), termination_criteria)
            image_points.append(corners)
        else:
            print("Corners could not be found in " + image_path + "! Removing...")
            try:
                os.remove(image_path)
            except:
                logging.getLogger().error("Error deleting file " + image_path, exc_info=True)

        if draw_image:
            cv2.drawChessboardCorners(image, grid_size, corners, has_corners)
            cv2.imshow(image_directory, image)
            sleep(.1)

        cv2.waitKey(1)  # TODO determine if I can safely put this into the if-statement.

    print("Found corners in {0} out of {1} images".format(len(image_points), len(images)))

    return object_points, image_points, camera_size


def get_matching_points(requested_file_names, all_file_names, object_points, image_points):
    """
        Gets the object points and image points of a requested set of files

    :param requested_file_names: files to look through
    :param all_file_names: the list of file names
    :param object_points: the object points list of the images in the given directory
    :param image_points: the image points list of the images in the given directory
    :return: the requested object points and image points
    """
    requested_file_nameset = set(requested_file_names)
    requested_object_points = []
    requested_image_points = []

    for index, filename in enumerate(all_file_names):
        if filename in requested_file_nameset:
            requested_object_points.append(object_points[index])
            requested_image_points.append(image_points[index])

    return requested_object_points, requested_image_points


# Find the chessboards on the left and right images.
(left_object_points, left_image_points, left_camera_size) = find_chessboards(left_camera_directory)
(right_object_points, right_image_points, left_camera_size) = find_chessboards(right_camera_directory)

object_points = left_object_points

###############################
# Calibration begins

print("calibrating left camera...")
_, leftCameraMatrix, leftDistortionCoefficients, _, _ = cv2.calibrateCamera(
    object_points, left_image_points, left_camera_size, None, None)
print("Done")
print("calibrating right camera...")
_, rightCameraMatrix, rightDistortionCoefficients, _, _ = cv2.calibrateCamera(
    object_points, right_image_points, left_camera_size, None, None)
print("Done")
# rotationMatrix is the rotation between coordinate systems of the first and second cameras
# translationVector is the translation between the coordinate systems of the two cameras
print("calibrating stereo cameras...")
(_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(
    object_points, left_image_points, right_image_points,
    leftCameraMatrix, leftDistortionCoefficients,
    rightCameraMatrix, rightDistortionCoefficients,
    left_camera_size, None, None, None, None,
    cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)
print("Done")
print("Starting stereo rectification...")
# Rectification matrices are the 3x3 rotation matrices for each of the two cameras
# Project matrices are the new rectified coordinate systems for each of the two cameras
# Q is the disparity to depth mapping
(leftRectification, rightRectification, leftProjection, rightProjection,
 Q_matrix, left_roi, right_roi) = cv2.stereoRectify(
    leftCameraMatrix, leftDistortionCoefficients,
    rightCameraMatrix, rightDistortionCoefficients,
    left_camera_size, rotationMatrix, translationVector,
    None, None, None, None, None,
    cv2.CALIB_ZERO_DISPARITY, OPTIMIZE_ALPHA)
print("Done")
# X and y maps are the projection maps
print("Saving the stereo calibration...")
left_xmap, left_ymap = cv2.initUndistortRectifyMap(
    leftCameraMatrix, leftDistortionCoefficients, leftRectification,
    leftProjection, left_camera_size, cv2.CV_32FC1)
right_xmap, right_ymap = cv2.initUndistortRectifyMap(
    rightCameraMatrix, rightDistortionCoefficients, rightRectification,
    rightProjection, left_camera_size, cv2.CV_32FC1)

np.savez_compressed(out_file1, image_size=left_camera_size,
                    left_xmap=left_xmap, left_ymap=left_ymap, left_roi=left_roi,
                    right_xmap=right_xmap, right_ymap=right_ymap, right_roi=right_roi, Q_matrix=Q_matrix)

np.savez_compressed(out_file2, leftRectification=leftRectification, rightRectification=rightRectification,
                    leftProjection=leftProjection, rightProjection=rightProjection,
                    Q_matrix=Q_matrix)
cv2.destroyAllWindows()
print("Done")


def run_calibration(square_size, grid_shape,
                    options=(cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK | cv2.CALIB_CB_ADAPTIVE_THRESH),
                    term_criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001),
                    optimize_alpha=0.25,
                    draw_image=True):
    """
    Calibrates the cameras.
    For accurate calibration, the chessboard pattern must be printed extremely accurately (laser-printer recommended).
    TODO: Flesh out calibration process in documentation.
    :param square_size: The real size of each chessboard square, in meters.
    :param grid_shape: The shape of the grid of internal chessboard squares, as a 2-tuple of the form (x_size, y_size).
    :param options: OpenCV2 option flags that specify how calibration is actually conducted. TODO: Clarify
    :param term_criteria: Termination criteria for various iterative calibration processes. TODO: Clarify
    :param optimize_alpha: TODO: Figure out what this even is
    :param draw_image: If True, displays each image as it is processed with the detected chessboard corners overlaid.
    """
    ###

    object_points_zero = get_object_points(grid_shape[0], grid_shape[1])


if __name__ == "__main__":
    CHESSBOARD_SQUARE_SIZE = .024
    CHESSBOARD_GRID_SHAPE = (6, 9)
    run_calibration(CHESSBOARD_SQUARE_SIZE, CHESSBOARD_GRID_SHAPE)
