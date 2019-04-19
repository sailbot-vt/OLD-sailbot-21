import numpy as np
import cv2
from . Depth_Map import Depth_Map as Depth

class DistanceCalculator():

    def __init__(self, calibrationDirectory, baseline = .2, focal_length = 56, DRAW_IMAGE = False):

        self.baseline = baseline
        self.focal_length = focal_length
        self.DRAW_IMAGE = DRAW_IMAGE
        self.RED_ORANGE_LOW = np.array([0, 150, 150])
        self.RED_ORANGE_HIGH = np.array([15, 255, 255])
        self.PURPLE_RED_LOW = np.array([160, 100, 100])
        self.PURPLE_RED_HIGH = np.array([180, 255, 255])
        self.kernel = np.ones((7, 7), np.uint8)
        self.depth_calculator = Depth(calibrationDirectory, DRAW_IMAGE = False)


    def findBuoyPixels(self):
        """
        Determine if the left camera has an image of the of buoy in it using color and shape. The calibration setup
        has the left camera as the primary camera, so the disparity map pixels are equivalent to the ones in the disparity map.

        :return:
        The pixels in which we see the buoy
        """
        image = self.depth_calculator.calculateDepthMap()
        #image mask
        hsv = cv2.Color(image, cv2.COLOR_BAYER_BG2BGR)
        hsv = cv2.GaussianBlur(hsv, (15,15),0)
        orange_red = cv2.inRange(hsv, self.RED_ORANGE_LOW, self.RED_ORANGE_HIGH)
        purple_red = cv2.inRange(hsv, self.PURPLE_RED_LOW, self.PURPLE_RED_HIGH)
        mask = orange_red + purple_red

        opened_mask = cv2.dilate(mask, self.kernel)

        __, cnts, __ = cv2.findContours(opened_mask.copy(), cv2.RETR_TREE. cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) == 0:
            print("Contours not found")
            if self.DRAW_IMAGE:
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
            return None


    def getDisparityValue(self, xPixel, yPixel):
        disparity = self.depth_calculator.calculateDepthMap()

        if disparity is None:
            return None

        #If the detected center pixel is near the edges, return just the disparity of that one pixel
        if xPixel <= 1 or yPixel <= 1 or xPixel >= 639 or yPixel >= 479:
            return disparity[xPixel][yPixel]
        #Otherwise, return the average of the surrounding pixels for a little more accuracy
        array = disparity[xPixel - 1: xPixel + 1, yPixel - 1: yPixel + 1]
        return sum(array)/array.size

    def getDistance(self,disparity_value):
        """
        Get the distance of the given disparity value using the two cameras' offsets, as well as the focal length and the calculated dispairty value
        :param disparity_value: the value of the disparity map that we use to calculate distance

        :return:
        the distance in meters of the given disparity
        """
        #D:= Distance of point in real world,
        #b:= base offset, (the distance *between* your cameras)
        #f:= focal length of camera,
        #d:= disparity:

        #D = b*f/d
        return self.baseline*self.focal_length/disparity_value


dist = DistanceCalculator("/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/stereo_calibration.npz")
dist.getDisparity(50,50)
