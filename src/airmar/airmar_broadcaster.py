from abc import ABC, abstractmethod
from enum import Enum
from pubsub import pub


class AirmarBroadcasterType(Enum):
    Testable = 0,
    Messenger = 1


class AirmarBroadcaster(ABC):
    """An abstract class to hide the interface required to notify the rest of the system of airmar input events.
    Messages are async to prevent them from blocking eachother, since RC input may need a high priority."""

    @abstractmethod
    def update_data(self, data=None):
        """ Updates data dictionary with new dictionary. """
        pass

    @abstractmethod
    def read_data(self, key=None):
        """ Reads the data currently stored in data dictionary.
        
        Keyword Arguments:
        key -- The id that matches key in dictionary
            Default: None
        
        Returns:
        Matching data value of key, or data dictionary if key is not
        provided or invalid
        """
        pass


class TestableAirmarBroadcaster(AirmarBroadcaster):
    """ A broadcaster built to test methods that need to broadcast."""

    def __init__(self):
        self.data = None

    def update_data(self, data=None):
        if data is not None:
            self.data = data

    def read_data(self, key=None):
        if self.data is not None:
            if key is not None and self.data.has_key(key):
                return self.data[key]
        # Returns entire data dictionary if no key/invalid key provided
        return self.data


class AirmarMessenger(AirmarBroadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast airmar data."""

    def update_data(self, data=None):
        if data is not None:
            self.data = data

    def read_data(self, key=None):
        """ Publishes data to pubsub. 
        
        Keyword Arguments:
        key -- The id that matches key in dictionary
            Default: None

        Returns:
        None if no key is provided/invalid
        data from map if successfully published
        """
        if key is None or not self.data.has_key(key):
            return None
        value = self.data[key]
        pub.sendMessage(topicName="set {}".format(key), msgData=value)
        return value


def make_broadcaster(broadcaster_type=None):
    """Creates a new, implementation-relevant AirmarBroadcaster.

    Implements the factory pattern.

    Keyword arguments:
    broadcaster_type -- The type of broadaster to create

    Returns:
    The correct AirmarBroadcaster for the environment.
    """
    if broadcaster_type == AirmarBroadcasterType.Messenger:
        return AirmarMessenger()

    return TestableAirmarBroadcaster()
