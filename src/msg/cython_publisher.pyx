from pickle import Pickler


cdef extern from "publisher.h":
    publish(char* channel_name, void* data, size_t data_size)


def _publish(channel_name, data):
    """Publishes data to a channel.

    Keyword arguments:
    channel_name -- The name of the channel to publish to
    data -- The data to send along the channel
    """
    pickled_data = Pickler(data)

    cdef size_t data_size = <int>sizeof(pickled_data)
    cdef void* data_ptr = <void*>pickled_data

    publish(channel_name, data_ptr, data_size)
