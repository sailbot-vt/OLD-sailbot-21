from abc import ABC, abstractmethod
from navigation_mode import NavigationMode


class RCBroadcaster(ABC):
    """An abstract class to hide the interface required to notify the rest of the system of RC input events.
    Messages are async to prevent them from blocking each other, since RC input may need a high priority."""

    @abstractmethod
    async def change_trim(self, degrees_in=0):
        """Broadcasts changes in trim to the system.

        Keyword arguments:
        degrees_in -- The number of degrees to trim in the sail. To let the sail out, enter a negative value.
        """
        pass

    @abstractmethod
    async def move_rudder(self, degrees_starboard=0):
        """Broadcasts rudder movements to the system.

        Keyword arguments:
        degrees_starboard -- The number of degrees to turn to starboard. To turn to port, enter a negative value.
        """
        pass

    @abstractmethod
    async def change_mode(self, mode=NavigationMode.MANUAL.value):
        """Broadcasts mode changes to the system.

        Keyword arguments:
        mode -- The new mode.
        """
        pass


class TestBroadcaster(RCBroadcaster):
    """A broadcaster built to test methods that need to broadcast."""
    async def change_trim(self, degrees_in=0):
        # Fake a message to change the trim
        pass

    async def move_rudder(self, degrees_starboard=0):
        # Fake a message to move the rudder
        pass

    async def change_mode(self, mode=NavigationMode.MANUAL.value):
        # Fake a message to change the mode
        pass


class RCMessenger(RCBroadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast RC input."""

    async def change_trim(self, degrees_in=0):
        # Send a message to change the trim
        pass

    async def move_rudder(self, degrees_starboard=0):
        # Send a message to move the rudder
        pass

    async def change_mode(self, mode=NavigationMode.MANUAL.value):
        # Send a message to change the mode
        pass

def make_broadcaster():
    """Creates a new, implementation-relevant RCBroadcaster.

    Implements the abstract factory pattern, except calls constructors instead of factory methods.

    Returns:
    The correct RCBroadcaster for the environment."""
    pass
