from abc import ABC, abstractmethod

from pubsub import pub

from src.navigation_mode import NavigationMode
from src.autonomy.nav.captain import Captain

class Event(ABC):
    """Base event type"""

    def __init__(self, tracker, boat, wind):
        """Creates a new event"""
        pub.subscribe(self.switch_mode, "set nav mode")

        self.create_objectives()
        self.create_event_config()

        self.captain = Captain(self.objectives, tracker, boat, wind, self.event_config)
        self.captain.start()

    @abstractmethod
    def read_interval(self):
        """Reads update interval from config"""
        pass

    @abstractmethod
    def create_objectives(self):
        """
        Sets list of objectives for Fleet Race
        """
        pass

    @abstractmethod
    def create_event_config(self):
        """
        Sets event configuration for fleet race
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
