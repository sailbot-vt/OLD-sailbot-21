from src.buoy_detection.Depth_Map_Calculator import DepthMap
import math
from numpy import rad2deg


def get_disparity_value(disparity_frame, x_pixel, y_pixel):
    """

    TODO: Find out if this logic has an advantage over the raw disparity map

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

    y_size, x_size = disparity_frame.shape[:2]

    # If the detected center pixel is near the edges, return just the disparity of that one pixel
    if x_pixel <= 0 or y_pixel <= 0 or x_pixel >= x_size - 1 or y_pixel >= y_size - 1:
        return disparity_frame[y_pixel][x_pixel]

    # Otherwise, return the average of the surrounding pixels for a little more accuracy
    array = disparity_frame[y_pixel - 1: y_pixel + 1, x_pixel - 1: x_pixel + 1]
    return array.sum() / array.size


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
            The distance in meters of the given disparity, or `math.inf` if the given disparity
            is zero.
        """

        if disparity_value == 0:
            return math.inf

        return (self.baseline * self.depth_map_calculator.focal_length) / disparity_value

    def get_bearing_from_pixel(self, x_pixel, cameras_rotation=0):
        """
        Calculate the boat-centered bearing of an object of interest (such as a buoy) by specifying its x-coordinate in
        the camera frame.

        Inputs:
            x_pixel -- the pixel in the x direction in which we see the buoy
            real_bearing -- the real bearing of the boat as read by the airmar
            cameras_rotation -- the rotation of the two cameras around the central axis, in degrees.

        Returns:
            The predicted bearing of the buoy taking into consideration the real bearing of the boat.
        """

        # Math from https://math.stackexchange.com/questions/1320285/convert-a-pixel-displacement-to-angular-rotation
        # x         := x-distance from center of the image in pixels (left / CCW = positive).
        # theta     := 1/2 horizontal field of view (radians)
        # b         := total number of pixels in x-direction.
        #
        # bearing = arctan(2x * tan(theta) / b)

        b = self.depth_map_calculator.image_size[0]
        x = b / 2 - x_pixel  # Left of the center is positive.

        theta = self.depth_map_calculator.hfov_rads / 2

        bearing_rads = math.atan(2 * x * math.tan(theta) / b)

        bearing_degs = rad2deg(bearing_rads) + cameras_rotation

        # Calculate equivalent bearing in range [-180, 180).
        # Works because:
        # We know bearing_degs + 180 should be in [0, 360), so we modulo by 360 to ensure that.
        # Finally, we subtract 180 to correct for the +180 we added earlier.
        return ((bearing_degs + 180) % 360) - 180
