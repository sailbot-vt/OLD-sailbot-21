import numpy as np
import cv2
from src.buoy_detection.Depth_Map_Calculator import Depth_Map
from math import sin, cos, asin, atan2, pi
import os
class DistanceCalculator():
    path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "stereo_calibration.npz"

    def __init__(self, calibration_directory = path, camera_baseline=.4064, camera_numbers=(2,3), DRAW_IMAGE = False):

        self.DRAW_IMAGE = DRAW_IMAGE
        self.depth_map_calculator = Depth_Map(calibration_directory, baseline = camera_baseline, camera_numbers=camera_numbers, DRAW_IMAGE = DRAW_IMAGE)

    def isBuoyInImage(self, left_frame):
        """
        Returns boolean value of if a large orange contour (buoy) is found in a frame
        :param left_frame: the frame from the main camera
        :return: boolean if buoy is found
        """
        kernel_close = np.ones((2, 2))
        kernel_open = np.ones((12, 12))

        hsv = cv2.cvtColor(left_frame, cv2.COLOR_BGR2HSV)

        # mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
        mask = cv2.inRange(hsv, (10, 100, 20), (15, 255, 255))
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask = mask_open
        mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
        mask = mask_close
        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours) > 0

    def findBuoyPixels(self, left_frame):
        """
        Determine if the left camera has an image of the of buoy in it using color. The calibration setup
        has the left camera as the primary camera, so the disparity map pixels are equivalent to the ones in the disparity map.

        :return:
        The pixels in which we see the buoy
        """

        kernel_close = np.ones((2, 2))
        kernel_open = np.ones((12, 12))

        frame_copy = left_frame

        hsv = cv2.cvtColor(left_frame, cv2.COLOR_BGR2HSV)

        # mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
        mask = cv2.inRange(hsv, (10, 100, 20), (15, 255, 255))
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask = mask_open
        mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
        mask = mask_close
        contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            biggest = sorted(contours, key=cv2.contourArea)[-1]
            if self.DRAW_IMAGE:
                cv2.drawContours(left_frame, contours, -1, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(biggest)
                cv2.rectangle(left_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            moment = cv2.moments(biggest)
            return int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])
        raise Exception("No buoy found in image")
        return None

    def getDisparityValue(self, disparity_frame, xPixel, yPixel):
        """
        Gets the disparity value from the disparity matrix if it is near an edge. Otherwise, gets an average of disparity values from surrounding pixels

        :param xPixel: the x coordinate in the disparity map
        :param yPixel: the y coordinate in the disparity map
        :return: the disparity value
        """

        if disparity_frame is None:
            print("disparity is None")
            return None

        #If the detected center pixel is near the edges, return just the disparity of that one pixel
        if xPixel <= 1 or yPixel <= 1 or xPixel >= 639 or yPixel >= 479:
            return disparity_frame[xPixel][yPixel]

        #Otherwise, return the average of the surrounding pixels for a little more accuracy
        array = disparity_frame[xPixel - 1: xPixel + 1, yPixel - 1: yPixel + 1]
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



    def getBearingFromxPixel(self, xPixel, real_bearing, cameras_rotation=0):
        """

        :param xPixel: the pixel in the x direction in which we see the buoy
        :param real_bearing: the real bearing of the boat as read by the airmar
        :param cameras_rotation: the rotation of the two cameras around the central axis (this is currently not implemented, so defaults to 0)
        :return: the predicted bearing of the buoy taking into consideration the real bearing of the boat
        """
        distance_from_center = xPixel - self.depth_map_calculator.image_size[0]/2
        relative_bearing = distance_from_center*self.depth_map_calculator.pixel_degrees

        camera_bearing = real_bearing + cameras_rotation
        new_bearing = camera_bearing + relative_bearing
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
        earth_radius = 6371000
        distance = distance / earth_radius
        # First attempt (might work?)
        # buoy_lat = asin(sin(boat_lat) * cos(distance) + cos(boat_lat) * sin(distance) * cos(bearing))
        # d_lon = atan2(sin(bearing) * sin(distance) * cos(boat_lat), cos(distance) - sin(boat_lat) * sin(buoy_lat))
        # buoy_lon = ((boat_lon - d_lon + pi) % 2 * pi) - pi
        # return np.rad2deg(buoy_lat), np.rad2deg(buoy_lon)


        # Here is another version if the previous isn't working well
        lat2 = asin(sin(boat_lat) * cos(distance) + cos(boat_lat) * sin(distance) * cos(bearing))
        a = atan2(sin(bearing) * sin(distance) * cos(boat_lat), cos(distance) - sin(boat_lat) * sin(lat2))
        lon2 = boat_lon + a
        lon2 = (lon2 + 3 * pi) % (2 * pi) - pi

        return np.rad2deg(lat2), np.rad2deg(lon2)
