from threading import Thread, Lock
from time import sleep

from pubsub import pub

from src.navigation_mode import NavigationMode
from src.nav.tack_points import place_tacks
from src.nav.config_reader import read_interval
from src.nav.course import Course, Path
from src.autopilot.autopilot import Autopilot


mutex = Lock()


class Captain(Thread):
    """Thread to manage autonomous navigation"""

    def __init__(self, boat, world, buoy_detection=False):
        """Builds a new captain thread."""
        super().__init__()
        self.boat = boat
        self.world = world
        self.is_active = True
        self.nav_interval = read_interval()
        self.autopilot = Autopilot(boat, world)
        if buoy_detection:
            self.course = Path()
        else:
            self.course = Course()
        pub.subscribe(self.switch_mode, "set nav mode")

    def run(self):
        """Runs the captain thread"""
        print("Started captain thread")
        while True:
            if self.is_active:
                mutex.acquire()
                course = iter(self.course)
                mutex.release()

                leg = course.current_leg()
                if len(self.autopilot.route) is 0:
                    leg = course.next_leg()

                self.autopilot.new_route(place_tacks(self.boat.current_position, leg[1], self.boat, self.world.wind))
                self.autopilot.activate()

                sleep(self.nav_interval)
            else:
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
        self.course.clear()

    def enable(self):
        """Enables the autonomous navigation"""
        self.is_active = True

    def drop_mark(self):
        """Adds a waypoint to the course"""
        mutex.acquire()
        self.course.add_mark(self.boat.current_position)
        mutex.release()

    def clear_course(self):
        mutex.acquire()
        self.course = Course()
        mutex.release()
