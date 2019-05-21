from threading import Thread
from time import sleep
from pubsub import pub

from src.gps_point import GPSPoint

from src.autopilot.route import Route
from src.autopilot.helmsman import Helmsman
from src.autopilot.config_reader import read_gain, read_interval


class Autopilot(Thread):
    """Manages the steering of the boat in autonomous mode."""

    @property
    def target_heading(self):
        """The current target heading"""
        if self.route.current_waypoint is None:
            return self.world.wind_direction  # If no target, turn head to wind

        return self.route.current_waypoint.bearing_from(self.boat.current_position)

    def __init__(self, boat, world):
        """Builds a new autopilot."""
        super().__init__()
        self.boat = boat
        self.world = world
        self.route = Route()
        self.helmsman = Helmsman(rudder_gain=read_gain())
        self.keep_running = True
        self.helm_interval = read_interval()
        pub.subscribe(self.add_to_route, "waypoints")

    def run(self):
        """Runs the autopilot thread"""
        while self.keep_running:
            self.update_route()
            self.helmsman.turn_to(self.target_heading, self.boat)
            sleep(self.helm_interval)

    def update_route(self):
        """Checks to see if we can remove a waypoint"""
        if GPSPoint.distance(self.route.current_waypoint, self.boat.current_position) < 1:
            self.route.next_waypoint()

    def add_to_route(self, waypoints):
        """Adds waypoints to the route"""
        self.route.add_waypoints(waypoints)
