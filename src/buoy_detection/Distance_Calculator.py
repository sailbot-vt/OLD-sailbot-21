import numpy as np
import cv2
from src.buoy_detection.Depth_Map_Calculator import DepthMap
from math import sin, cos, asin, atan2, pi
import os


def is_buoy_in_image(frame):
    """
    Returns boolean value of if a large orange contour (buoy) is found in a frame
    :param frame: the frame from the main camera (normally the left camera)
    :return: boolean if buoy is found
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


def get_disparity_value(disparity_frame, x_pixel, y_pixel):
    """

    *** UNUSED CURRENTLY *** TODO: Find out if this logic has an advantage over the raw disparity map

    Gets the disparity value from the disparity matrix if it is near an edge.
    Otherwise, gets an average of disparity values from surrounding pixels.

    :param disparity_frame: the raw disparity data, in the form of an image.
    :param x_pixel: the x coordinate in the disparity map
    :param y_pixel: the y coordinate in the disparity map
    :return: the disparity value
    """

    if disparity_frame is None:
        print("disparity is None")
        return None

    # If the detected center pixel is near the edges, return just the disparity of that one pixel
    if x_pixel <= 1 or y_pixel <= 1 or x_pixel >= 639 or y_pixel >= 479:
        return disparity_frame[x_pixel][y_pixel]

    # Otherwise, return the average of the surrounding pixels for a little more accuracy
    array = disparity_frame[x_pixel - 1: x_pixel + 1, y_pixel - 1: y_pixel + 1]
    return sum(array)/array.size


def get_obj_gps_location(boat_lat, boat_lon, distance, bearing):
    """
    Gets the predicted gps location of an object based on the current gps location,
    angle to the object, and the distance to the object.

    The math was found from here:
    https://stackoverflow.com/questions/19352921/how-to-use-direction-angle-and-speed-to-calculate-next-times-latitude-and-longi

    :param boat_lat:  the current latitude of the boat in radians
    :param boat_lon:  the current longitude of the boat in radians
    :param distance:  the predicted distance to the object in meters
    :param bearing:  the bearing (angle) to the object in radians
    :return: A 2-tuple containing the boat's latitude and longitude, in degrees.
    """
    # Earth radius in meters
    earth_radius = 6371000

    # Calculate angular distance (theta = distance / radius)
    ang_distance = distance / earth_radius

    # First attempt (might work?)
    # obj_lat = asin(sin(boat_lat) * cos(distance) + cos(boat_lat) * sin(distance) * cos(bearing))
    # d_lon = atan2(sin(bearing) * sin(distance) * cos(boat_lat), cos(distance) - sin(boat_lat) * sin(obj_lat))
    # obj_lon = ((boat_lon - d_lon + pi) % 2 * pi) - pi
    # return np.rad2deg(obj_lat), np.rad2deg(obj_lon)

    # Here is another version if the previous isn't working well
    # TODO Check math
    lat2 = asin(sin(boat_lat) * cos(ang_distance) + cos(boat_lat) * sin(ang_distance) * cos(bearing))
    a = atan2(sin(bearing) * sin(ang_distance) * cos(boat_lat), cos(ang_distance) - sin(boat_lat) * sin(lat2))
    lon2 = boat_lon + a
    lon2 = (lon2 + 3 * pi) % (2 * pi) - pi

    return np.rad2deg(lat2), np.rad2deg(lon2)


class DistanceCalculator:
    default_calibration_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "stereo_calibration.npz"

    def __init__(self, calibration_path=default_calibration_path, camera_offset=.4064, camera_numbers=(2, 3),
                 draw_image=False):
        """
        :param calibration_path: The path of the calibration data, stored in .npz format.
        :param camera_offset: The distance between the left and right cameras in meters.
        :param camera_numbers: Which USB ports the cameras are plugged into, in the format (left_cam_number,
                right_cam_number).
        :param draw_image: Whether or not to show depth maps and draw object outlines.
            TODO Determine what DepthMap's draw_image does
        """

        self.draw_image = draw_image

        # How far apart the cameras are.
        self.base_offset = camera_offset

        self.depth_map_calculator = \
            DepthMap(calibration_path, baseline=camera_offset, camera_numbers=camera_numbers,
                     draw_image=draw_image)

    def find_buoy_pixels(self, frame):
        """
        Determine if the given frame has an image of the of buoy in it using color. The calibration setup
        has the left camera as the primary camera, so the disparity map pixels are equivalent to the ones in
        the disparity map.

        TODO split buoy-specific code into separate function and create generic object-outlining function.

        :return: The pixels in which we see the buoy
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
            if self.draw_image:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(biggest)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            moment = cv2.moments(biggest)
            return int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])
        raise Exception("No buoy found in image")

    def get_distance(self, disparity_value):
        """
        Get the distance of the given disparity value using the two cameras' offsets, as well as the focal length and
        the calculated disparity value.
        :param disparity_value: the value of the disparity map that we use to calculate distance.

        :return:
        The distance in meters of the given disparity
        """
        # D:= Distance of point in real world,
        # b:= base offset, (the distance *between* your cameras)
        # f:= focal length of camera,
        # d:= disparity:

        # D = b*f/d
        return (self.base_offset * self.depth_map_calculator.focal_length) / disparity_value

    def get_bearing_from_pixel(self, x_pixel, real_bearing, cameras_rotation=0):
        """
        Calculate the absolute bearing of an object of interest (such as a buoy) by specifying its x-coordinate in
        the camera frame.

        :param x_pixel: the pixel in the x direction in which we see the buoy
        :param real_bearing: the real bearing of the boat as read by the airmar
        :param cameras_rotation: the rotation of the two cameras around the central axis (this is currently not
                implemented, so defaults to 0)
        :return: the predicted bearing of the buoy taking into consideration the real bearing of the boat
        """
        # TODO Verify that the image_size tuple is of the form (x_size, y_size) and not the other way around
        distance_from_center = x_pixel - self.depth_map_calculator.image_size[0] / 2

        # TODO Verify that angles actually work like this with the camera frame.
        relative_bearing = distance_from_center * self.depth_map_calculator.pixel_degrees

        camera_bearing = real_bearing + cameras_rotation
        new_bearing = camera_bearing + relative_bearing

        # Calculate equivalent bearing in range [0, 360). The "+ 360" is necessary in case we begin with a negative
        # value for `new_bearing`.
        return ((new_bearing % 360) + 360) % 360
