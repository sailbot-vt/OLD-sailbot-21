# distutils: sources = consumer.c relay.c

from cpython.ref cimport PyObject

cdef extern register_to_consume_data(int channelName, PyObject* callback)

cdef cython_subscribe(channelName, dataCallback):

    cdef int C_channelName = <int>channelName

    cdef PyObject* callback = <PyObject*>dataCallback

    register_to_consume_data(C_channelName, callback)


def subscribe(self, channelName, dataCallback):

    """
    Register with relay to receive a callback upon data being received on <channel_name>. 

    Calls cython which calls the C... Relay keeps track of who to signal upon receiving new data

    Keyword arguments:
    channel_name -- The name of the channel to subscribe to (need to coordinate with producer to have matching values)
    data_callback -- Method to execute upon receiving signal from relay... This method will be passed the dereferenced data from shared memory
    """

    cython_subscribe(channelName, dataCallback)
