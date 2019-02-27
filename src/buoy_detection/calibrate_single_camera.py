import cv2
import numpy as np
import os
import glob


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
                cv2.drawChessboardCorners(img, (7, 6), corners, ret)
                cv2.imshow('img', img)
                k = cv2.waitKey(33)
                if k == 27:
                    break

#Create a calibration matrix that can be saved and used to quickly undistort images
def calibrate(camera_number, camera_width, camera_height, image_path):

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    for filename in os.listdir(image_path):
        if ".jpg" in filename:
            curr = image_path + filename
            img = cv2.imread(curr)
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(grey, (7, 6), None)

            if ret:
                objpoints.append(objp)
                cv2.cornerSubPix(grey, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, grey.shape[::-1], None, None)
    img = cv2.imread(image_path + "IMG_0.jpg")
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    return newcameramtx, roi


def main():
    #Create image correction matrix and roi
    image_path = generate_images(0, 1280, 720)
    test_view_checkerboard(0, 1280, 720, image_path)
    matrix, roi = calibrate(0, 1280, 720, image_path)



main()