import cv2
import numpy as np
csc = __import__("calibrate_single_camera")

def stereo_calibrate(camera_number1, camera_width1, camera_height1, camera_number2, camera_width2, camera_height2):
    image_path1 = csc.generate_images(camera_number1, camera_width1, camera_height1)
    (left_new_mtx, left_roi, left_mtx, left_objpoints, left_imagepoints) = csc.calibrate(camera_number1, camera_width1, camera_height1, image_path1)

    image_path2 = csc.generate_images(camera_number2, camera_width2, camera_height2)
    (right_new_mtx, right_roi, right_mtx, right_objpoints, right_imagepoints) = csc.calibrate(camera_number2, camera_width2, camera_height2, image_path2)

    (_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(
        left_objpoints, left_imagepoints, right_imagepoints,
        left_mtx, left_new_mtx,
        right_mtx, right_new_mtx,
        (camera_height1, camera_width1), None, None, None, None)


    #Return calibration

def main():
    stereo_calibrate(0, 1920, 1080, 0, 1920, 1080)

main()
#def save_stereo_calibration(calibration):
#    np.savez_compressed(outputFile, imageSize=imageSize,
#                        leftMapX=leftMapX, leftMapY=leftMapY, leftROI=leftROI,
#                        rightMapX=rightMapX, rightMapY=rightMapY, rightROI=rightROI)
#def rectify_image():