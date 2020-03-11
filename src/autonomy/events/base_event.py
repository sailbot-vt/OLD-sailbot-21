from abc import ABC, abstractmethod

from threading import Thread, Lock
from pubsub import pub

from src.navigation_mode import NavigationMode
from src.autonomy.nav.captain import Captain

mutex = Lock()


class Event(ABC, Thread):
    """Base event type"""

    def __init__(self, boat, wind):
        """Creates a new event"""
        pub.subscribe(self.switch_mode, "set nav mode")

        self.create_objectives()

        self.captain = Captain(self.objectives, boat, wind)
        self.captain.start()

    @abstractmethod
    def run(self):
        """Runs event thread"""
        pass

    @abstractmethod
    def read_interval(self):
        """Reads update interval from config"""
        pass

    @abstractmethod
    def create_objectives(self):
        """
        Creates objectives based on enumerations
        """
        pass

    def switch_mode(self, mode):
        """
        Changes the navigation mode
        Inputs:
            mode -- navigation mode to switch to
        """
        if mode is NavigationMode.AUTONOMOUS:
            self.enable()
        else:
            self.disable()

    def enable(self):
        """Enables autonomous navigation"""
        self.captain = Captain()
        self.captain.start()

    def disable(self):
        """
        Disable autonomous navigation
        """   
        self.captain.quit()
