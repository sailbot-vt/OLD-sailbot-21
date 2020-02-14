from threading import Thread, Lock
from time import sleep
import math

from pubsub import pub

from src.autopilot.route import Route
from src.autopilot.helmsman import Helmsman
from src.autopilot.config_reader import read_gain, read_interval, long_tol, lat_tol


mutex = Lock()


class Autopilot(Thread):
    """Manages the steering of the boat in autonomous mode."""

    @property
    def target_heading(self):
        """The current target heading"""
        if self.route.current_waypoint is None:
            return self.world.wind.true_wind_angle  # If no target, turn head to wind

        return self.route.current_waypoint.bearing_from(self.boat.current_position)

    def __init__(self, boat, world):
        """Builds a new autopilot."""
        super().__init__()
        self.boat = boat
        self.world = world
        self.route = Route()
        self.helmsman = Helmsman(rudder_gain=read_gain())
        self.helm_interval = read_interval()
        self.long_tol = long_tol()
        self.lat_tol = lat_tol()
        self.on_standby = False
        pub.subscribe(self.add_to_route, "waypoints")

    def run(self):
        """Runs the autopilot thread"""
        print("Started autopilot")
        while True:
            if not self.on_standby:
                self.update_route()
                self.helmsman.turn_to(self.target_heading, self.boat)

                # Call to sail.turn_to_angle(...)
                # Should use self.world.wind.true_wind_angle or .apparent_wind_angle

                sleep(self.helm_interval)

    def update_route(self):
        """Checks to see if we can remove a waypoint"""
        mutex.acquire()
        lat_dist = math.fabs(self.route.current_waypoint.lat - self.boat.current_position.lat)
        long_dist = math.fabs(self.route.current_waypoint.long - self.boat.current_position.long)
        if lat_dist < self.lat_tol and long_dist < self.long_tol:
            self.route.next_waypoint()
        mutex.release()

    def add_to_route(self, waypoints):
        """Adds waypoints to the route"""
        mutex.acquire()
        self.route.add_waypoints(waypoints)
        mutex.release()

    def new_route(self, waypoints):
        """Replaces waypoints on the route"""
        mutex.acquire()
        self.route.add_waypoints(waypoints)
        mutex.release()

    def standby(self):
        """Sets the autopilot to standby"""
        self.on_standby = True

    def activate(self):
        """Reactivates the autopilot from standby"""
        self.on_standby = False
