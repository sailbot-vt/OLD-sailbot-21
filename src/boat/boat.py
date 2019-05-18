from pubsub import pub

from src.gps_point import GPSPoint


class Boat:
    """Holds information about the boat"""

    def polar_speed(self, apparent_wind):
        pass

    @property
    def max_heel_angle(self):
        return 0

    @property
    def current_position(self):
        """Gets the current position of the boat"""
        return self._current_position

    def __init__(self):
        """Builds a new boat"""
        self._current_position = GPSPoint(0, 0)
        pub.subscribe(self.read_latitude, "boat latitude")
        pub.subscribe(self.read_longitude, "boat longitude")

    def read_latitude(self, latitude):
        """Updates the boat's latitude"""
        self._current_position.lat = latitude

    def read_longitude(self, longitude):
        """Updates the boat's longitude"""
        self._current_position.long = longitude
