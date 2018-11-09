# distutils: sources = consumer.c relay.c

cdef extern register_to_consume_data(int channelName, PyObject callback)

def subscribe(self, channel_name, data_callback):

    """
    Register with relay to receive a callback upon data being received on <channel_name>. 

    Calls cython which calls the C... Relay keeps track of who to signal upon receiving new data

    Keyword arguments:
    channel_name -- The name of the channel to subscribe to (need to coordinate with producer to have matching values)
    data_callback -- Method to execute upon receiving signal from relay... This method will be passed the dereferenced data from shared memory
    """

    register_to_consume_data(channelName, data_callback)


