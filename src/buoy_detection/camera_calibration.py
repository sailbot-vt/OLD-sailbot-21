import cv2
import numpy as np
import os


# Calibrate a single camera by taking pictures of a printed out checkerboard
# This checkerboard is compared using opencv2's built in calibration functions
# Chessboard address: https://docs.opencv2.org/2.4/_downloads/pattern.png


# Generate images of a checkerboard that will be used to calibrate camera
def generate_images(cam_number, cam_width, cam_height):

    # Capturee images from the LEFT camera
    if cam_number == 0:
        image_path = "./camera_capture/LEFT/"

    # Capture images from the RIGHT camera
    elif cam_number == 1:
        image_path = "./camera_capture/RIGHT/"
    else:
        raise Exception("Please input a valid camera number")

    cam = cv2.VideoCapture(cam_number)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

    #While you are setting up checkerboard, turn the camera on and wait for the space bar
    while (cv2.waitKey(33) != ord(" ")):
        (grabbed, frame) = cam.read()
        cv2.putText(frame, "Press Space to start recording", (10,500), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2)
        cv2.imshow("Generate_Images", frame)
        if cv2.waitKey(33) == 27:
            cv2.release()
            cv2.destroyAllWindows()
            break

    #Once you press space, record 20 frames
    frame_id = 0
    while (frame_id < 20):
        (grabbed, frame) = cam.read()
        if not grabbed:
            cam.release()
            cv2.destroyAllWindows()
            raise Exception("Camera image could not be taken")

        cv2.imwrite(image_path + "IMG_" + str(frame_id) + ".jpg", frame)
        cv2.imshow("generate images", frame)
        if cv2.waitKey(33) == 27:
            break
        frame_id += 1

    cam.release()
    cv2.destroyAllWindows()

    return image_path

#Shows the output of opencv trying to detect a checkerboard on screen
#This function searches through the given directory for images, and does its best to look for the checkerboard in each image
def test_view_checkerboard(image_path):
    for filename in os.listdir(image_path):
        if ".jpg in filename":
            curr = image_path + filename
            img = cv2.imread(curr)
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(grey, (7, 6), None)
            if ret:
                cv2.drawChessboardCorners(img, (10,7), corners, ret)
                cv2.imshow('img', img)
                k = cv2.waitKey(33)
                if k == 27:
                    break

#Create a calibration matrix that can be saved and used to quickly undistort images
def calibrate(camera_number, camera_width, camera_height, image_path):

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    c_rows = 6
    c_cols = 9
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((c_rows*c_cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:c_cols, 0:c_rows].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    for filename in os.listdir(image_path):
        if ".jpg" in filename:
            curr = image_path + filename
            img = cv2.imread(curr)
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(grey, (6,9), None)

            if ret:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(grey, corners, (11,11), (-1, -1), criteria)
                imgpoints.append(corners)
                cv2.drawChessboardCorners(img, (7,6), corners2, ret)
                cv2.imshow("frame", img)
                cv2.waitKey(200)
    if len(objpoints) <= 1:
        raise Exception("Chessboard corners not detected!")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, grey.shape[::-1], None, None)
    img = cv2.imread(image_path + "IMG_0.jpg")
    h, w = img.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    return (new_camera_matrix, roi, mtx, objpoints, imgpoints)



def stereo_calibrate(camera_number1, camera_width1, camera_height1, camera_number2, camera_width2, camera_height2):



    stereo_calibration_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 1e-5)
    stereo_calibration_flags = cv2.CALIB_FIX_INTRINSIC


    image_path1 = generate_images(camera_number1, camera_width1, camera_height1)
    (left_distortion_coeff, left_roi, left_mtx, left_objpoints, left_imagepoints) = calibrate(
        camera_number1,
        camera_width1,
        camera_height1,
        image_path1)

    image_path2 = generate_images(camera_number2, camera_width2, camera_height2)
    (right_distortion_coeff, right_roi, right_mtx, right_objpoints, right_imagepoints) = calibrate(
        camera_number2,
        camera_width2,
        camera_height2,
        image_path2)


    stereocalibration_retval, left_mtx, left_distortion_coeff, \
    right_mtx, right_distortion_coeff, R, T, E, F = cv2.stereoCalibrate(
        left_objpoints,
        left_imagepoints,
        right_imagepoints,
        left_mtx,
        left_distortion_coeff,
        right_mtx,
        right_distortion_coeff,
        (camera_height1, camera_width1),
        criteria=stereo_calibration_criteria,
        flags=stereo_calibration_flags)


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

    return (camera_height1, camera_width1, left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi)


def stereo_test():
    (camera_height1, camera_width1, left_xmap, left_ymap, left_roi, right_xmap, right_ymap, right_roi) = stereo_calibrate(0, 640, 480, 0, 640, 480)
    np.savez_compressed("./x", camera_height1, camera_width1, left_xmap, left_ymap, left_roi, right_xmap, right_ymap,
                        right_roi)
    cal = np.load("./x.npz", allow_pickle=True)
    print(cal["leftMapX"])
    # image_size = tuple(calibration["image_size"])
    # leftMapX = calibration["leftMapX"]
    # leftMapY = calibration["leftMapY"]
    # leftROI = tuple(calibration["leftROI"])
    # rightMapX = calibration["rightMapX"]
    # rightMapY = calibration["rightMapY"]
    # rightROI = tuple(calibration["rightROI"]
def run():
    cal = np.load("./x.npz", allow_pickle=False)
    print(cal['arr_1'])
    #['arr_7', 'arr_2', 'arr_1', 'arr_4', 'arr_5', 'arr_0', 'arr_6', 'arr_3']

#def mono_test():
#    image_path = generate_images(0, 1920, 1080)
#    (new_mtx, roi, mtx, None, None) = calibrate(0, 1920, 1080, image_path)


run()