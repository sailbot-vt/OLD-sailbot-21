import numpy as np
from src.buoy_detection.Depth_Map_Calculator import DepthMap
from math import sin, cos, asin, atan2, pi


def get_disparity_value(disparity_frame, x_pixel, y_pixel):
    """

    *** UNUSED CURRENTLY *** TODO: Find out if this logic has an advantage over the raw disparity map

    Gets the disparity value from the disparity matrix if it is near an edge.
    Otherwise, gets an average of disparity values from surrounding pixels.

    Inputs:
        disparity_frame -- The raw disparity data, in the form of an image.
        x_pixel -- The x coordinate in the disparity map.
        y_pixel -- The y coordinate in the disparity map.

    Returns:
        The disparity value.
    """

    if disparity_frame is None:
        print("disparity is None")
        return None

    # If the detected center pixel is near the edges, return just the disparity of that one pixel
    if x_pixel <= 1 or y_pixel <= 1 or x_pixel >= 639 or y_pixel >= 479:
        return disparity_frame[x_pixel][y_pixel]

    # Otherwise, return the average of the surrounding pixels for a little more accuracy
    array = disparity_frame[x_pixel - 1: x_pixel + 1, y_pixel - 1: y_pixel + 1]
    return sum(array) / array.size


def get_obj_gps_location(boat_lat, boat_lon, distance, bearing):
    """
    Gets the predicted gps location of an object based on the current gps location,
    angle to the object, and the distance to the object.

    The math was found from here:
    https://stackoverflow.com/questions/19352921/how-to-use-direction-angle-and-speed-to-calculate-next-times-latitude-and-longi

    Inputs:
        boat_lat -- the current latitude of the boat in radians
        boat_lon -- the current longitude of the boat in radians
        distance -- the predicted distance to the object in meters
        bearing -- the bearing (angle) to the object in radians

    Returns:
         A 2-tuple containing the boat's latitude and longitude, in degrees.
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
    def __init__(self, master_config):
        """Initialize the DistanceCalculator.

        Inputs:
            master_config -- A loaded master buoy_detection YAML configuration (use config_reader).
        """
        # How far apart the cameras are.
        self.baseline = master_config["common"]["baseline"]

        self.depth_map_calculator = DepthMap(master_config)

    def get_distance(self, disparity_value):
        """
        Get the distance of the given disparity value using the two cameras' offsets, as well as the focal length and
        the calculated disparity value.

        D := Distance of point in real world
        b := Baseline, the distance *between* your cameras
        f := focal length of camera
        d := disparity value

        D = b*f/d

        Inputs:
            disparity_value -- The value of the disparity map that we use to calculate distance.

        Returns:
            The distance in meters of the given disparity.
        """

        return (self.baseline * self.depth_map_calculator.focal_length) / disparity_value

    def get_bearing_from_pixel(self, x_pixel, real_bearing, cameras_rotation=0):
        """
        Calculate the absolute bearing of an object of interest (such as a buoy) by specifying its x-coordinate in
        the camera frame.

        Inputs:
            x_pixel -- the pixel in the x direction in which we see the buoy
            real_bearing -- the real bearing of the boat as read by the airmar
            cameras_rotation -- the rotation of the two cameras around the central axis (this is currently not
                                implemented, so defaults to 0)

        Returns:
            The predicted bearing of the buoy taking into consideration the real bearing of the boat.
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
