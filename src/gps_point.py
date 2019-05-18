import math
from src.utils import vec


class GPSPoint:
    """Stores a single GPS point"""

    def __init__(self, lat, long):
        """Builds a new GPS point"""
        self.pt = vec.Vec2(long, lat)
        self.lat = self.pt.y
        self.long = self.pt.x

    def bearing_from(self, gps_point):
        """Gets the bearing from a different GPS point.

        Returns:
        The bearing that, at the other GPS point, you would travel to get to this point"""
        if self.long == gps_point.long:
            cartesian_angle = 90 if gps_point.lat <= self.lat else -90
        else:
            cartesian_angle = 180 * math.atan((self.lat - gps_point.lat) / (self.long - gps_point.long)) / math.pi
            if self.long < gps_point.long:
                cartesian_angle -= 180

        return GPSPoint.convert_to_bearing(cartesian_angle)

    @staticmethod
    def convert_to_bearing(cartesian_angle):
        """Converts a Cartesian angle to a compass bearing.

        Cartesian angles are angles in R^2 with 0deg along the positive x-axis and increasing counterclockwise. Compass
        bearings are angles in R^2 with 0deg along the positive y-axis and increasing clockwise.

        Keyword arguments:
        cartesian_angle -- The Cartesian angle to convert

        Returns:
        The compass bearing corresponding to the ray defined by the Cartesian angle
        """
        return (90 - cartesian_angle) % 360
