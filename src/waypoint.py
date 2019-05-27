from src.gps_point import GPSPoint


class Waypoint(GPSPoint):
    """A course waypoint"""

    def is_upwind_of(self, other):
        """Checks if the other point is upwind of this point"""
        return self.lat > other.lat
