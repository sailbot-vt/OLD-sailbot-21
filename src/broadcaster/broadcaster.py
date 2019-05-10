from abc import ABC, abstractmethod
from enum import Enum
from pubsub import pub


class BroadcasterType(Enum):
    Testable = 0,
    Messenger = 1,
    FileWriter = 2


class Broadcaster(ABC):
    """An abstract class to hide the interface required to notify the rest of the system of airmar input events.
    Messages are async to prevent them from blocking eachother, since RC input may need a high priority."""

    @abstractmethod
    def update_data(self, data=None):
        """ Updates data dictionary with new dictionary. Data must be packaged into dictionary such that
        key represents data type, value represents data. """
        pass

    @abstractmethod
    def read_data(self, key=None):
        """ Reads the data currently stored in data dictionary.
        
        Keyword Arguments:
        key -- The id that matches key in dictionary
            Default: None
        """
        pass


class TestableBroadcaster(Broadcaster):
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


class Messenger(Broadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast data."""

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


class FileWriter(Broadcaster):
    """Implements an interface to write data to file. """

    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def update_data(self, data=None):
        if data is not None:
            self.data = data
    
    def read_data(self, key=None):
        # TODO finish
        pass


def make_broadcaster(broadcaster_type=None):
    """Creates a new broadcaster.

    Implements the factory pattern.

    Keyword arguments:
    broadcaster_type -- The type of broadaster to create

    Returns:
    The correct broadcaster for the environment.
    """
    if broadcaster_type == BroadcasterType.Messenger:
        return Messenger()

    return TestableBroadcaster()
