from pubsub import pub

from src.gps_point import GPSPoint
from src.boat.config_reader import upwind_angle


class Boat:
    """Holds information about the boat"""

    @property
    def current_position(self):
        """Gets the current position of the boat"""
        return self._current_position

    @property
    def current_heading(self):
        return self._current_heading

    @property
    def current_speed(self):
        return self._current_speed

    @property
    def current_sensor_ang(self):
        return self._current_sensor_ang

    @property
    def current_sensor_vel(self):
        return self._current_sensor_vel

    @property
    def current_sail_ang(self):
        return self._current_sail_ang

    @property
    def current_rudder_ang(self):
        return self._current_rudder_ang

    @property
    def current_jib_ang(self):
        return self._current_jib_ang

    @property
    def current_rear_foil_ang(self):
        return self._current_rear_foil_ang

    def __init__(self):
        """Builds a new boat"""
        self.upwind_angle = upwind_angle()
        self._current_heading = 0
        self._current_position = GPSPoint(0, 0)
        pub.subscribe(self.read_latitude, "boat latitude")
        pub.subscribe(self.read_longitude, "boat longitude")
        pub.subscribe(self.read_heading, "boat heading")
        pub.subscribe(self.read_speed, "boat speed")
        pub.subscribe(self.read_sensor_ang, "sensor angle")
        pub.subscribe(self.read_sensor_vel, "sensor vel")
        pub.subscribe(self.read_sail_ang, "sail angle")
        pub.subscribe(self.read_rudder_ang, "rudder angle")
        pub.subscribe(self.read_jib_ang, "jib angle")
        pub.subscribe(self.read_rear_foil_ang, "rear_foil angle")
        print("Boat ready\nupwind_angle={0}".format(self.upwind_angle))

    def read_latitude(self, latitude):
        """Updates the boat's latitude"""
        self._current_position.lat = latitude

    def read_longitude(self, longitude):
        """Updates the boat's longitude"""
        self._current_position.long = longitude

    def read_heading(self, heading):
        """Updates the boat's current heading"""
        self._current_heading = heading

    def read_speed(self, speed):
        """Updates the boat's current speed"""
        self._current_speed = speed

    def read_sensor_ang(self, ang):
        """Updates the boat's current sensor angle"""
        self._current_sensor_ang = ang

    def read_sensor_vel(self, vel):
        """Updates the boat's current sensor angle"""
        self._current_sensor_vel = vel

    def read_sail_ang(self, ang):
        """Updates the boat's current sail angle"""
        self._current_sail_ang = ang

    def read_rudder_ang(self, ang):
        """Updates the boat's current rudder angle"""
        self._current_rudder_ang = ang

    def read_jib_ang(self, ang):
        """Updates the boat's current jib angle"""
        self._current_jib_ang = ang

    def read_rear_foil_ang(self, ang):
        """Updates the boat's current rear foil angle"""
        self._current_rear_foil_ang = ang
