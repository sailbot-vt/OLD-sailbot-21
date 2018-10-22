from abc import ABC, abstractmethod

class producer(ABC):
    """
    An abstract class to hide the interface with Cython from producers
    """

    @abstractmethod
    def register_to_produce_data(self, channel_name, data_size, buffer_length):
        """
        Register with relay to produce data... Relay assigns a pointer to shared memory for it to publish to

        Channel name and data pointer location is stored in hash table by relay, where it can be accessed later by both consumers and producers

        Keyword arguments:
        channel_name -- The name of the channel to publish to (need to coordinate with consumers to have matching values
        data_size -- Size of the data to be passed to relay
        buffer_size -- Used in conjunction with data_size to determine total size of shared memory to be assigned to this channel
        """

        self.channel_name = channel_name
        self.data_size = data_size
        self.buffer_length = buffer_length
#       cython_register_to_produce_data(channel_name, data_size, buffer_length)
        pass

    @abstractmethod
    def publish_data(channel_name=self.channel_name, data)
        """
        Push data to shared memory through cython

        Data will be converted to bytearray before pushed to memory

        Keyword arguments:
        channel_name -- The name of the channel to publish to
        data -- Data to be published to shared memory
        """


#       cython_publish_data(channel_name, self.data_size, data)
        pass

class example_producer_class(producer):
    """
    Inherits from producer base class
    """
    def register_to_produce_data(self, channel_name):
        """
        Nothing additional needed here... Just remember to run this method in order to be able to publish data
        """
        
        pass

    def publish_data(channel_name = self.channel_name, data)
        """
        Nothing additional needed here... Remember to consider datatype before pushing
        """

        pass

