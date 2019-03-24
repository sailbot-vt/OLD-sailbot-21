import glob
import os
import numpy as np
import cv2

CHESSBOARD_CALIBRATION_SIZE = (6, 9)
CHESSBOARD_OPTIONS = (cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK | cv2.CALIB_CB_ADAPTIVE_THRESH)

#Required size for cv2
OBJECT_POINT_ZERO = np.zeros((CHESSBOARD_CALIBRATION_SIZE[0] * CHESSBOARD_CALIBRATION_SIZE[1], 3), np.float32)
OBJECT_POINT_ZERO[:, :2] = np.mgrid[0:CHESSBOARD_CALIBRATION_SIZE[0],0 : CHESSBOARD_CALIBRATION_SIZE[1]].T.reshape(-1, 2)

#subject to change
OPTIMIZE_ALPHA = 0.25

TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30,0.001)


left_camera_directory = "C:/Users/Wylans xps 13/PycharmProjects/SailBOT19/src/buoy_detection/camera_capture/LEFT"
right_camera_directory = "C:/Users/Wylans xps 13/PycharmProjects/SailBOT19/src/buoy_detection/camera_capture/RIGHT"
out_file = "C:/Users/Wylans xps 13/PycharmProjects/SailBOT19/src/buoy_detection/camera_capture/stereo_calibration.npz"

def findChessboards(imageDirectory):
    """
    Calculates the object points and image points of chessboard images
    :param imageDirectory: the directory to look through for chessboard images
    :return: names of the files, the object points list, the image points list, resolution of the camera
    """
    out_file = "{0}/chessboards.npz".format(imageDirectory)
    print("Reading images at {0}".format(imageDirectory))
    images = glob.glob("{0}/*.jpg".format(imageDirectory))

    file_names = []
    object_points = []
    image_points = []
    left_camera_size = None

    for image_path in sorted(images):
        image = cv2.imread(image_path)
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        left_camera_size = image_grey.shape[::-1]

        has_corners, corners = cv2.findChessboardCorners(image_grey, CHESSBOARD_CALIBRATION_SIZE, cv2.CALIB_CB_FAST_CHECK)

        if has_corners:
            file_names.append(os.path.basename(image_path))
            object_points.append(OBJECT_POINT_ZERO)
            cv2.cornerSubPix(image_grey, corners, (11, 11), (-1, -1), TERMINATION_CRITERIA)
            image_points.append(corners)
        cv2.drawChessboardCorners(image, CHESSBOARD_CALIBRATION_SIZE, corners, has_corners)
        cv2.imshow(imageDirectory, image)

        cv2.waitKey(1)

    cv2.destroyWindow(imageDirectory)

    print("Found corners in {0} out of {1} images".format(len(image_points), len(images)))

    np.savez_compressed(out_file, file_names = file_names, object_points = object_points, image_points = image_points, imageSize = left_camera_size)
    return file_names, object_points, image_points, left_camera_size


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


(left_file_names, left_object_points, left_image_points, left_camera_size) = findChessboards(left_camera_directory)
(right_file_names, right_object_points, right_image_points, left_camera_size) = findChessboards(right_camera_directory)

file_names = sorted(list(set(left_file_names) & set(right_file_names)))

left_object_points, left_image_points = get_matching_points(file_names,
        left_file_names, left_object_points, left_image_points)

right_object_points, right_image_points = get_matching_points(file_names,
        right_file_names, right_object_points, right_image_points)

object_points = left_object_points

print("calibrating left camera")
_, leftCameraMatrix, leftDistortionCoefficients, _, _ = cv2.calibrateCamera(
        object_points, left_image_points, left_camera_size, None, None)

print("calibrating right camera")
_, rightCameraMatrix, rightDistortionCoefficients, _, _ = cv2.calibrateCamera(
        object_points, right_image_points, left_camera_size, None, None)

print("calibrating stereo cameras")
(_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(
        object_points, left_image_points, right_image_points,
        leftCameraMatrix, leftDistortionCoefficients,
        rightCameraMatrix, rightDistortionCoefficients,
        left_camera_size, None, None, None, None,
        cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

print("Starting stereo rectification")

(leftRectification, rightRectification, leftProjection, rightProjection,
        __, left_roi, right_roi) = cv2.stereoRectify(
                leftCameraMatrix, leftDistortionCoefficients,
                rightCameraMatrix, rightDistortionCoefficients,
                left_camera_size, rotationMatrix, translationVector,
                None, None, None, None, None,
                cv2.CALIB_ZERO_DISPARITY, OPTIMIZE_ALPHA)

print("Saving the stereo calibration")
left_xmap, left_ymap = cv2.initUndistortRectifyMap(
        leftCameraMatrix, leftDistortionCoefficients, leftRectification,
        leftProjection, left_camera_size, cv2.CV_32FC1)
right_xmap, right_ymap = cv2.initUndistortRectifyMap(
        rightCameraMatrix, rightDistortionCoefficients, rightRectification,
        rightProjection, left_camera_size, cv2.CV_32FC1)

np.savez_compressed(out_file, image_size=left_camera_size,
        left_xmap=left_xmap, left_ymap=left_ymap, left_roi=left_roi,
        right_xmap=right_xmap, right_ymap=right_ymap, right_roi=right_roi)

cv2.destroyAllWindows()