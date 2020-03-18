import numpy as np

from pubsub import pub

from src.utils.vec import Vec2
from src.utils.polar_distance import polar_distance

class Wind:
    """A unified API for all wind data"""

    @property
    def true_wind(self):
        """Gets the latest true wind reading

        Returns:
        A Vec2 of the true wind
        """
        return self._true_wind

    @property
    def apparent_wind(self):
        """Gets the latest apparent wind reading

        Returns:
        A Vec2 of the apparent wind
        """
        return self._apparent_wind

    def __init__(self):
        """Builds a new wind object"""
        self.true_wind_speed = 0
        self.true_wind_angle = 0
        self.apparent_wind_speed = 0
        self.apparent_wind_angle = 0
        self._true_wind = Vec2(0, 0)
        self._apparent_wind = Vec2(0, 0)

        pub.subscribe(self.update_true_wind_angle, "wind angle true")
        pub.subscribe(self.update_true_wind_speed, "wind speed true")
        pub.subscribe(self.update_apparent_wind_angle, "wind angle apparent")
        pub.subscribe(self.update_apparent_wind_speed, "wind speed apparent")

    def update_true_wind_angle(self, angle):
        """Updates the true wind angle"""
        self.true_wind_angle = angle
        self._true_wind = Vec2.build_from(self.true_wind_speed, angle)

    def update_true_wind_speed(self, speed):
        """Updates the true wind speed"""
        self.true_wind_speed = speed
        self._true_wind = Vec2.build_from(speed, self.true_wind_angle)

    def update_apparent_wind_angle(self, angle):
        """Updates the apparent wind angle"""
        self.apparent_wind_angle = angle
        self._apparent_wind = Vec2.build_from(self.apparent_wind_speed, angle)

    def update_apparent_wind_speed(self, speed):
        """Updates the apparent wind speed"""
        self.apparent_wind_speed = speed
        self._apparent_wind = Vec2.build_from(speed, self.apparent_wind_angle)

    def angle_relative_to_wind(self, bearing):
        """Converts a bearing into a relative wind angle

        Returns:
        A angle between -179 and 180
        """
        angle = self.true_wind_angle - bearing
        return 360 + angle if angle <= -180 else angle

    def distance_upwind(self, start, end):
        """Gives the upwind distance to end.

        If boat is upwind of end, the result if negative."""
        path_dist = polar_distance((start, end))
        # account for undefined behavior of bearing when range is 0
        if start[0] == 0 and end[0] == 0:
            path_bearing = 0
        elif start[0] == 0 and end[0] != 0:
            path_bearing = end[1]
        elif start[0] != 0 and end[0] == 0:
            path_bearing = (start[1] - 180) % 360
        else:
            path_bearing = end[1] - start[1]
        angle_difference = self.angle_relative_to_wind(path_bearing)
        return path_dist * np.cos(np.radians(angle_difference))
