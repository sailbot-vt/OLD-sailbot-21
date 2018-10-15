from abc import ABC, abstractmethod

class consumer(ABC):
    """
    An abstract class to hide the interface with Cython from consumers.
    """

    @abstractmethod
    def register_to_consume_data(self, channel_name, data_callback=self.data_callback)
        """
        Register with relay to receive a callback upon data being received on <channel_name>. 

        Calls cython which calls the C... Relay keeps track of who to signal upon receiving new data

        Keyword arguments:
        channel_name -- The name of the channel to subscribe to (need to coordinate with producer to have matching values)
        data_callback -- Method to execute upon receiving signal from relay... This method will be passed the dereferenced data from shared memory
        """

#       cython_register_to_consume_data(channel_name, data_callback)
        pass
    
    @abstractmethod
    def data_callback(self, data):
        """
        This method is instantiated upon receiving a signal from the relay

        Called by cython method that dereferences data in shared memory and passes it to this function

        Keyword arguments:
        data -- Data that is passed to the callback... Will likely be in a structured numpy array
        """

        pass


class example_consumer_class(consumer):
    """
    Inherits from consumer abstract base class
    """
    def register_to_consume_data(self, channel_name):
        """
        Nothing additional needed here... Just remember to run this method in order to receive any data!
        """

        pass

    def data_callback(self, data)
        """
        Do any processing needed on the data... Remember to keep the system real-time
        """
        pass

