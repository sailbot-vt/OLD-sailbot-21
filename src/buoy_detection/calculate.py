import numpy as np
import cv2
#Distance between cameras in meters
baseline = 1
#Lower focal length
fx_low = 56
#Higher focal length
fx_high = 76
DRAW_IMAGE = True
matrices = np.load("/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/projection_matrices.npz", allow_pickle=False)

leftRectification = matrices['leftRectification']
rightRectification= matrices['rightRectification']
leftProjection= matrices['leftProjection']
rightProjection= matrices['rightProjection']
Q_matrix= matrices['Q_matrix']
print("\n\nleftRect")
print(leftRectification)
print("\n\nleftproj")
print(leftProjection)
print("\n\nQ")
print(Q_matrix)



def findBuoy(image):
    RED_ORANGE_LOW = np.array([0, 150, 150])
    RED_ORANGE_HIGH = np.array([15, 255, 255])
    PURPLE_RED_LOW = np.array([160, 100, 100])
    PURPLE_RED_HIGH = np.array([180, 255, 255])
    kernel = np.ones((7,7), np.uint8)

    #image mask
    hsv = cv2.Color(image, cv2.COLOR_BAYER_BG2BGR)
    hsv = cv2.GaussianBlur(hsv, (15,15),0)
    orange_red = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
    purple_red = cv2.inRange(hsv, PURPLE_RED_LOW, PURPLE_RED_HIGH)
    mask = orange_red + purple_red

    opened_mask = cv2.dilate(mask, kernel)

    __, cnts, __ = cv2.findContours(opened_mask.copy(), cv2.RETR_TREE. cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        print("Contours not found")
        if DRAW_IMAGE:
            cv2.imshow_split(opened_mask, image, title = "Window")
    cnt = max(cnts, key = cv2.contourArea)

    cnt = cv2.convexHull(cnt)
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
    else:
        print("No Moments found")
        cv2.imshow_split(opened_mask, image, title = "Moments")