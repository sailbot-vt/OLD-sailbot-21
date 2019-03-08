import cv2
import numpy as np

#Calculates a distance matrix for each pixel on the screen, given a disparity matrix
def calculate_distance_matrix(camera_offset, focal_length, disparity):
    return (camera_offset*focal_length)/disparity


def isolate_buoy(img):
    RED_ORANGE_MIN = np.array([0, 150, 150])
    RED_ORANGE_MAX = np.array([15, 255, 255])
    PURPLE_RED_MIN = np.array([160, 100, 100])
    PURPLE_RED_MAX = np.array([180, 255, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (15, 15), 0)

    orange_red_mask = cv2.inRange(hsv, cv2.RED_ORANGE_MIN, cv2.RED_ORANGE_MAX)
    purpe_red_mask = cv2.inRange(hsv, PURPLE_RED_MIN, PURPLE_RED_MAX)
    mask = orange_red_mask + purpe_red_mask