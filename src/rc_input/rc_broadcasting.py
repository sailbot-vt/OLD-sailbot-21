from abc import ABC, abstractmethod
from src.navigation_mode import NavigationMode


class RCBroadcaster(ABC):
    """An abstract class to hide the interface required to notify the rest of the system of RC input events.
    Messages are async to prevent them from blocking each other, since RC input may need a high priority."""

    @abstractmethod
    def change_trim(self, degrees_in=0):
        """Broadcasts changes in trim to the system.

        Keyword arguments:
        degrees_in -- The number of degrees to trim in the sail. To let the sail out, enter a negative value.
        """
        pass

    @abstractmethod
    def move_rudder(self, degrees_starboard=0):
        """Broadcasts rudder movements to the system.

        Keyword arguments:
        degrees_starboard -- The number of degrees to turn to starboard. To turn to port, enter a negative value.
        """
        pass

    @abstractmethod
    def change_mode(self, mode=NavigationMode.MANUAL.value):
        """Broadcasts mode changes to the system.

        Keyword arguments:
        mode -- The new mode.
        """
        pass


class TestableBroadcaster(RCBroadcaster):
    """A broadcaster built to test methods that need to broadcast."""
    def __init__(self):
        self.rudder_signals = []
        self.trim_signals = []
        self.mode_signals = []

    def change_trim(self, degrees_in=0):
        self.trim_signals.append(degrees_in)

    def move_rudder(self, degrees_starboard=0):
        self.rudder_signals.append(degrees_starboard)

    def change_mode(self, mode=NavigationMode.MANUAL.value):
        self.mode_signals.append(mode)


class RCMessenger(RCBroadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast RC input."""

    def change_trim(self, degrees_in=0):
        # Send a message to change the trim
        pass

    def move_rudder(self, degrees_starboard=0):
        # Send a message to move the rudder
        pass

    def change_mode(self, mode=NavigationMode.MANUAL.value):
        # Send a message to change the mode
        pass


def make_broadcaster():
    """Creates a new, implementation-relevant RCBroadcaster.

    Implements the abstract factory pattern, except calls constructors instead of factory methods.

    Returns:
    The correct RCBroadcaster for the environment."""
    return TestableBroadcaster()
