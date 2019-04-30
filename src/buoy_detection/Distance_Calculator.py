import numpy as np
import cv2
from src.buoy_detection.Depth_Map_Calculator import Depth_Map as Depth
from math import sin, cos, asin, atan2, pi
import os
class DistanceCalculator():
    path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "stereo_calibration.npz"

    def __init__(self, calibration_directory = path, DRAW_IMAGE = False):

        self.DRAW_IMAGE = DRAW_IMAGE
        self.RED_ORANGE_LOW = np.array([0, 150, 150])
        self.RED_ORANGE_HIGH = np.array([15, 255, 255])
        self.PURPLE_RED_LOW = np.array([160, 100, 100])
        self.PURPLE_RED_HIGH = np.array([180, 255, 255])
        self.kernel = np.ones((7, 7), np.uint8)
        self.depth_map_calculator = Depth(calibration_directory, DRAW_IMAGE = False)
        self.DRAW_IMAGE = DRAW_IMAGE

    def findBuoyPixels(self):
        """
        Determine if the left camera has an image of the of buoy in it using color and shape. The calibration setup
        has the left camera as the primary camera, so the disparity map pixels are equivalent to the ones in the disparity map.

        :return:
        The pixels in which we see the buoy
        """
        frame = self.depth_map_calculator.calculateDepthMap()
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        RED_ORANGE_LOW = np.array([100, 100, 0])
        RED_ORANGE_HIGH = np.array([255, 230, 200])
        kernel_open = np.ones((6, 6))
        kernel_close = np.ones((10, 10))

        mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)
        mask = mask_close

        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) <= 0:
            return None
        elif len(contours) > 0:
            biggest = sorted(contours, key=cv2.contourArea)[-1]
            if self.DRAW_IMAGE:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(biggest)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            moment = cv2.moments(biggest)
            return int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])


    def getDisparityValue(self, xPixel, yPixel):
        """
        Gets the disparity value from the disparity matrix if it is near an edge. Otherwise, gets an average of disparity values from surrounding pixels

        :param xPixel: the x coordinate in the disparity map
        :param yPixel: the y coordinate in the disparity map
        :return: the disparity value
        """
        disparity = self.depth_map_calculator.calculateDepthMap()

        if disparity is None:
            return None

        #If the detected center pixel is near the edges, return just the disparity of that one pixel
        if xPixel <= 1 or yPixel <= 1 or xPixel >= 639 or yPixel >= 479:
            return disparity[xPixel][yPixel]

        #Otherwise, return the average of the surrounding pixels for a little more accuracy
        array = disparity[xPixel - 1: xPixel + 1, yPixel - 1: yPixel + 1]
        return sum(array)/array.size

    def getDistance(self, disparity_value):
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
        return self.baseline*self.depth_map_calculator.focal_length/disparity_value


    def getBearingFromxPixel(self, xPixel, real_bearing):
        """

        :param xPixel: the pixel in the x direction in qhich we see the buoy
        :param real_bearing: the real bearing of the boat as read by the airmar
        :return: the predicted bearing of the buoy taking into consideration the real bearing of the boat
        """
        distance_from_center = xPixel - self.depth_map_calculator.image_size[0]/2
        relative_bearing = distance_from_center*self.depth_map_calculator.pixel_degrees

        new_bearing = real_bearing + relative_bearing
        return ((new_bearing % 360) + 360) % 360


    def getBuoyGPSLocation(self, boat_lat, boat_lon, distance, bearing):
        """
        Gets the predicted gps location of the buoy based on the current gps location, angle to the buoy, and the distance to the buoy

        The math was found from here:
        https://stackoverflow.com/questions/19352921/how-to-use-direction-angle-and-speed-to-calculate-next-times-latitude-and-longi

        :param boat_lat:  the current latitude of the boat
        :param boat_lon:  the current longitude of the boat
        :param distance:  the predicted distance to the buoy in meters
        :param bearing:  the bearing (angle) to the buoy in radians
        :return:
        """
        int
        earth_radius = 6371000;
        distance = distance / earth_radius
        # First attempt (might work?)
        # buoy_lat = asin(sin(boat_lat) * cos(distance) + cos(boat_lat) * sin(distance) * cos(bearing))
        # d_lon = atan2(sin(bearing) * sin(distance) * cos(boat_lat), cos(distance) - sin(boat_lat) * sin(buoy_lat))
        # buoy_lon = ((boat_lon - d_lon + pi) % 2 * pi) - pi
        # return np.rad2deg(buoy_lat), np.rad2deg(buoy_lon)


        # Here is another version if the previous isn't working well
        lat2 = asin(sin(boat_lat) * cos(distance) + cos(boat_lat) * sin(distance) * cos(bearing));
        a = atan2(sin(bearing) * sin(distance) * cos(boat_lat), cos(distance) - sin(boat_lat) * sin(lat2));
        lon2 = boat_lon + a;
        lon2 = (lon2 + 3 * pi) % (2 * pi) - pi;

        return np.rad2deg(lat2), np.rad2deg(lon2)

# Example usage:
#dist = DistanceCalculator("/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/stereo_calibration.npz")
#dist.getDisparity()
