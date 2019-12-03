from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from pubsub import pub


class BroadcasterType(Enum):
    Testable = 0,
    Messenger = 1,
    FileWriter = 2


class Broadcaster(ABC):
    """ An abstract class for interfaces required to notify the 
    rest of the system of input events. """

    def __init__(self):
        self.data = None

    def publish_dictionary(self, data):
        """ Updates data dictionary with new dictionary. 

        Keyword Arguments:
        data -- A dictionary containing key and value. 
        """
        self.data = data
        for key in self.data:
            self.publish_key(key=key)

    @abstractmethod
    def publish_key(self, key):
        """ Reads the data currently stored in data dictionary.
        
        Keyword Arguments:
        key -- The id that matches key in dictionary
            Default: None
        """
        pass


class TestableBroadcaster(Broadcaster):
    """ A broadcaster built to test methods that need to broadcast."""

    def __init__(self):
        """ Dictionary implementation of broadcaster."""
        super().__init__()

    def publish_key(self, key):
        """ Retrieves stored data. 
        
        Keyword Arguments:
        key -- The id that matches key in dictionary

        Returns:
        The data[key] value
        """
        return self.data[key]
        

class Messenger(Broadcaster):
    """Implements an interface with the pub/sub 
    messaging system to broadcast data."""

    def __init__(self):
        """ Messenger pubsub implementation of broadcaster."""
        super().__init__()

    def publish_key(self, key):
        """ Publishes data to pubsub. 
        
        Keyword Arguments:
        key -- The id that matches key in dictionary

        Returns:
        The msgData published to pubsub
        """
        value = self.data[key]
        pub.sendMessage(topicName="{}".format(key), msgData=value)
        return value


class FileWriter(Broadcaster):
    """Implements an interface to write data to file. """

    def __init__(self, filename):
        """ FileWriter implementation of broadcaster.

        Keyword Arguments:
        filename -- the name of the file to read/write to.
        """
        super().__init__()
        self.filename = filename
        self.line_format = "[{0:20s}]\t\t[Requested: {1} -- Data: {2}]\n"
    
    def publish_key(self, key):
        """ Publishes key value pair by appending to file. 
        
        Keyword Arguments:
        key -- The id that matches key in dictionary
        """
        f = open(self.filename, "a")

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
