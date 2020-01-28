from threading import Thread

from pubsub import pub

import numpy as np
import cv2

import src.buoy_detection.Distance_Calculator as dc
from src.waypoint import Waypoint
import logging


def find_buoy_pixels(frame, draw_image=False):
    """
    Determine if the given frame has an image of the of buoy in it using color. The calibration setup
    has the left camera as the primary camera, so the disparity map pixels are equivalent to the ones in
    the disparity map.

    Inputs:
        frame -- The color (BGR format) image to analyze.
        draw_image -- Whether or not to draw the buoy pixel contours after finding buoy pixels.

    TODO split buoy-specific code into separate function and create generic object-outlining function.

    Returns:
        The coordinates of the center of the largest buoy.
    """

    kernel_close = np.ones((2, 2))
    kernel_open = np.ones((12, 12))

    frame_copy = frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
    mask = cv2.inRange(hsv, (10, 100, 20), (15, 255, 255))
    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask = mask_open
    mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
    mask = mask_close
    contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        biggest = sorted(contours, key=cv2.contourArea)[-1]
        if draw_image:
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            x, y, w, h = cv2.boundingRect(biggest)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        moment = cv2.moments(biggest)
        return int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])
    raise Exception("No buoy found in image")


def is_buoy_in_image(frame):
    """
    Returns boolean value of if a large orange contour (buoy) is found in a frame.

    Inputs:
        frame -- The frame from the main camera (normally the left camera).

    Returns:
         Boolean representing if a buoy is found.
    """
    kernel_close = np.ones((2, 2))
    kernel_open = np.ones((12, 12))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask = cv2.inRange(hsv, RED_ORANGE_LOW, RED_ORANGE_HIGH)
    mask = cv2.inRange(hsv, (10, 100, 20), (15, 255, 255))
    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask = mask_open
    mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
    mask = mask_close
    contours, __ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours) > 0


class BuoyDetector(Thread):
    def __init__(self, boat):
        super().__init__()
        self.distance_calculator = dc
        self.buoy_location = None
        self.boat = boat

    def run(self):
        """Continuously checks for a buoy"""
        while True:
            try:
                left_frame, disparity_frame = self.distance_calculator.depth_map_calculator.calculate_depth_map()
            except Exception:
                logging.getLogger().error("Couldn't calculate depth map!", exc_info=True)
                continue

            try:
                # We use the left frame here because the left camera is our "primary camera."
                buoy_pixel_x, buoy_pixel_y = self.distance_calculator.find_buoy_pixels(left_frame)
            except Exception:
                logging.getLogger().error("Couldn't find buoy pixels!", exc_info=True)
                continue

            # Get the disparity value of the pixels found
            disparity_of_buoy = dc.get_disparity_value(disparity_frame, buoy_pixel_x, buoy_pixel_y)

            # Calculate the distance to the buoy using the disparity values
            distance_to_buoy = self.distance_calculator.get_distance(disparity_of_buoy)

            # Get a reading from airmar
            real_bearing_reading_from_airmar = self.boat.current_heading
            get_latitude_from_airmar = self.boat.current_position.lat
            get_longitude_from_airmar = self.boat.current_position.long

            calculated_bearing_to_buoy = \
                self.distance_calculator.get_bearing_from_pixel(buoy_pixel_x, real_bearing_reading_from_airmar)

            estimated_buoy_lat, estimated_buoy_long = \
                dc.get_obj_gps_location(get_latitude_from_airmar, get_longitude_from_airmar,
                                        distance_to_buoy, calculated_bearing_to_buoy)

            pub.sendMessage("buoy detected", location=Waypoint(estimated_buoy_lat, estimated_buoy_long))
