import cv2
import numpy as np
csc = __import__("calibrate_single_camera")

def stereo_calibrate(camera_number1, camera_width1, camera_height1, camera_number2, camera_width2, camera_height2):

    stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 1e-5)
    stereocalib_flags = cv2.CALIB_FIX_ASPECT_RATIO | cv2.CALIB_ZERO_TANGENT_DIST | cv2.CALIB_SAME_FOCAL_LENGTH | cv2.CALIB_RATIONAL_MODEL | cv2.CALIB_FIX_K3 | cv2.CALIB_FIX_K4 | cv2.CALIB_FIX_K5

    image_path1 = csc.generate_images(camera_number1, camera_width1, camera_height1)
    (left_distortion_coeff, left_roi, left_mtx, left_objpoints, left_imagepoints) = csc.calibrate(
        camera_number1,
        camera_width1,
        camera_height1,
        image_path1)

    image_path2 = csc.generate_images(camera_number2, camera_width2, camera_height2)
    (right_distortion_coeff, right_roi, right_mtx, right_objpoints, right_imagepoints) = csc.calibrate(
        camera_number2,
        camera_width2,
        camera_height2,
        image_path2)
    print("\nleft_mtx")
    print(left_mtx)
    print("\nright)_mtx")
    print(right_mtx)
    print("\nright_roi")
    print(right_roi)
    print("\nleft_roi")
    print(left_roi)
    #print("\nobject_points")
    #print(left_objpoints)
    print("\nleft_distortion")
    print(left_distortion_coeff)
    print("\nright_distortion")
    print(right_distortion_coeff)
    #print("\nLeft_image_points")
    #print(left_imagepoints)
    #print("\nRight_image_points")
    #print(right_imagepoints)

    stereocalibration_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 1e-5)
    stereocalibration_flags = cv2.CALIB_FIX_INTRINSIC

    stereocalibration_retval, left_mtx, left_distortion_coeff, right_mtx, right_distortion_coeff, R, T, E, F = cv2.stereoCalibrate(
        left_objpoints,
        left_imagepoints,
        right_imagepoints,
        left_mtx,
        left_distortion_coeff,
        right_mtx,
        right_distortion_coeff,
        (camera_height1, camera_width1),
        criteria=stereocalibration_criteria,
        flags=stereocalibration_flags)


    #Convert the calibration into matrices that can be used to directly correctly the stereo
    (leftRectification, rightRectification, leftProjection,
     rightProjection,
     disparity_to_depth_map,
     left_roi, right_roi) = cv2.stereoRectify(
        left_mtx,
        left_distortion_coeff,
        right_mtx,
        right_distortion_coeff,
        (camera_height1, camera_width1),
        R,
        T, alpha=1)

    left_xmap, left_ymap = cv2.initUndistortRectifyMap(
        left_mtx,
        left_distortion_coeff,
        leftRectification,
        leftProjection,
        (camera_height1, camera_width1),
        cv2.CV_32FC1)

    right_xmap, right_ymap = cv2.initUndistortRectifyMap(
        right_mtx,
        right_distortion_coeff,
        rightRectification,
        rightProjection,
        (camera_height1, camera_width1),
        cv2.CV_32FC1)

    return ((camera_height1, camera_width1), left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi)


def save_calibration(save_to, image_height, image_width, left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi):
    np.savez_compressed(save_to, (image_height, image_width), left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi)

def load_calibration(location):
    calibration = np.load(location, allow_pickle=False)
    print(calibration["left_mapx"])
    #image_size = tuple(calibration["image_size"])
    #leftMapX = calibration["leftMapX"]
    #leftMapY = calibration["leftMapY"]
    #leftROI = tuple(calibration["leftROI"])
    #rightMapX = calibration["rightMapX"]
    #rightMapY = calibration["rightMapY"]
    #rightROI = tuple(calibration["rightROI"]

def main():
    ((camera_height1, camera_width1), left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi) = stereo_calibrate(0, 640, 480, 0, 640, 480)
    save_calibration("./x", camera_height1, camera_width1, left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi)
    load_calibration("./x.npz")

main()
