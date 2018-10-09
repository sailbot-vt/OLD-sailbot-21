from abc import ABC, abstractmethod
from enum import Enum


class NavigationMode(Enum):
    """Semantically represents the navigation mode."""
    MANUAL = 0


class RCBroadcaster(ABC):
    """An abstract class to hide the interface with the pub/sub messaging system.
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