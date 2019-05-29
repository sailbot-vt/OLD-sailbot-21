from threading import Thread
from time import sleep

from pubsub import pub

from src.navigation_mode import NavigationMode
from src.nav.tack_points import place_tacks
from src.nav.config_reader import read_interval
from src.nav.course import Course
from src.autopilot.autopilot import Autopilot


class Captain(Thread):
    """Thread to manage autonomous navigation"""

    def __init__(self, boat, world):
        """Builds a new captain thread."""
        super().__init__()
        self.boat = boat
        self.world = world
        self.is_active = False
        self.nav_interval = read_interval()
        self.autopilot = Autopilot(boat, world)
        self.course = Course()
        pub.subscribe()

    def run(self):
        """Runs the captain thread"""
        print("Started captain thread")
        course = iter(self.course)
        while True:
            if self.is_active:
                if course is None:
                    course = iter(self.course)

                leg = course.current_leg()
                if len(self.autopilot.route) is 0:
                    leg = course.next_leg()

                self.autopilot.new_route(place_tacks(self.boat.current_position, leg[1], self.boat, self.world.wind))
                self.autopilot.activate()

                sleep(self.nav_interval)
            else:
                course = None
                self.autopilot.standby()

    def switch_mode(self, mode):
        """Changes the navigation mode"""
        if mode is NavigationMode.AUTONOMOUS:
            self.enable()
        else:
            self.disable()

    def disable(self):
        """Disables the autonomous navigation"""
        self.is_active = False

    def enable(self):
        """Enables the autonomous navigation"""
        self.is_active = True

    def drop_mark(self):
        """Adds a waypoint to the course"""
        self.course.add_mark(self.boat.current_position)
