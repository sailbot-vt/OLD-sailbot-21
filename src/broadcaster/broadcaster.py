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

    @abstractmethod
    def publish_dictionary(self, data):
        """ Publishes all key-value pair currently in the dictionary.

        Keyword Arguments:
        data -- A dictionary containing key and value. 
        """
        pass


class TestableBroadcaster(Broadcaster):
    """ A broadcaster built to test methods that need to broadcast."""

    def __init__(self):
        """ Dictionary implementation of broadcaster."""
        self.data = None

    def publish_dictionary(self, data):
        """ Saves data to broadcaster's dictionary """
        self.data = data
        

class Messenger(Broadcaster):
    """Implements an interface with the pub/sub 
    messaging system to broadcast data."""

    def __init__(self):
        """ Messenger pubsub implementation of broadcaster."""
        super().__init__()

    def publish_dictionary(self, data):
        """ Publishes all data to pubsub.

        Keyword Arguments:
        data -- The data dictionary containing key-value pair, where
                key is the topicName and value is the data to publish.
        """
        for key in data:
            pub.sendMessage(topicName="{}".format(key), msgData=data[key])


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
    
    def publish_dictionary(self, data):
        """ Writes a formated dictionary update to file.

        Keyword Arguments:
        data -- The data dictionary containing key-value pair to write to file.
        """
        f = open(self.filename, "a")

        for key in data:
            f.write(self.line_format.format(datetime.now().__str__(), key, data[key]))
        f.close()


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
