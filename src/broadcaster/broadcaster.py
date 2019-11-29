from abc import ABC, abstractmethod
from datetime import datetime
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
    def update_dictionary(self, data=None):
        """ Updates data dictionary with new dictionary. Data must be packaged into dictionary such that
        key represents data type, value represents data. """
        pass

    @abstractmethod
    def update_key(self, key=None):
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

    def update_dictionary(self, data=None):
        if data is not None:
            self.data = data
            for key in self.data.keys():
                self.update_key(key=key)

    def update_key(self, key=None):
        if self.data is None or key is None or not key in self.data or self.data[key] is None:
            return None
        return self.data[key]
        


class Messenger(Broadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast data."""

    def __init__(self):
        self.data = None

    def update_dictionary(self, data=None):
        if data is not None:
            self.data = data
            for key in self.data.keys():
                self.update_key(key=key)

    def update_key(self, key=None):
        """ Publishes data to pubsub. 
        
        Keyword Arguments:
        key -- The id that matches key in dictionary
            Default: None

        Returns:
        None if no key is provided/invalid, data/data[key] not initialized
        data from map if successfully published
        """
        if self.data is None or key is None or not key in self.data or self.data[key] is None:
            return None
        value = self.data[key]
        pub.sendMessage(topicName="set {}".format(key), msgData=value)
        return value


class FileWriter(Broadcaster):
    """Implements an interface to write data to file. """

    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.line_format = "[{0:20s}]\t\t[Requested: {1} -- Data: {2}]\n"

    def update_dictionary(self, data=None):
        if data is not None:
            self.data = data
            for key in self.data.keys():
                self.update_key(key=key)
    
    def update_key(self, key=None):
        # Appends to end of file.
        f = open(self.filename, "a")
        if self.data is None or key is None or not key in self.data or self.data[key] is None:
            return None
        value = self.data[key]
        f.write(self.line_format.format(datetime.now().__str__(), key, value))
        f.close()
        return value


def make_broadcaster(broadcaster_type=None, filename=None):
    """Creates a new broadcaster.

    Implements the factory pattern.

    Keyword arguments:
    broadcaster_type -- The type of broadaster to create
    filename -- File name of file to write data to.
        Default: None if not needed.

    Returns:
    The correct broadcaster for the environment.
    """
    if broadcaster_type == BroadcasterType.Messenger:
        return Messenger()
    if broadcaster_type == BroadcasterType.FileWriter:
        return FileWriter(filename)
    return TestableBroadcaster()
