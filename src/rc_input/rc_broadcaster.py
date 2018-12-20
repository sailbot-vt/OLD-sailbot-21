from abc import ABC, abstractmethod
from enum import Enum

import src.msg as msg
from src.navigation_mode import NavigationMode


class RCInputBroadcasterType(Enum):
    Testable = 0,
    Messenger = 1


class RCInputBroadcaster(ABC):
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


class TestableInputBroadcaster(RCInputBroadcaster):
    """A broadcaster built to test methods that need to broadcast."""
    def __init__(self):
        self.rudder_signals = []
        self.trim_signals = []
        self.mode_signals = []

    def change_trim(self, degrees_in=0):
        self.trim_signals.append(degrees_in)

    def move_rudder(self, degrees_starboard=0):
        self.rudder_signals.append(degrees_starboard)

    def change_mode(self, mode=NavigationMode.MANUAL):
        self.mode_signals.append(mode)


class RCInputMessenger(RCInputBroadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast RC input."""

    def change_trim(self, degrees_in=0):
        msg.publish("set trim", degrees_in)

    def move_rudder(self, degrees_starboard=0):
        msg.publish("set rudder", degrees_starboard)

    def change_mode(self, mode=NavigationMode.MANUAL):
        msg.publish("set nav mode", mode)


def make_broadcaster(broadcaster_type=RCInputBroadcasterType.Messenger):
    """Creates a new, implementation-relevant RCBroadcaster.

    Implements the factory pattern.

    Keyword arguments:
    broadcaster_type -- The type of broadcaster to create


    Returns:
    The correct RCBroadcaster for the environment."""
    if broadcaster_type == RCInputBroadcasterType.Messenger:
        return RCInputMessenger()

    return TestableInputBroadcaster()
