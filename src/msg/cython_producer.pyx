# distutils: sources = producer.c relay.c
# distutils: include_dirs = Python.h
from pickle import Pickler
from libc.stdlib cimport malloc


cdef extern register_to_produce_data(int channel_name, int data_size)
cdef extern publish_data(int channel_name, int data_size, int *source_ptr)
cdef extern deregister_to_produce_data(int channel_name)



def publish(channel_name, data):
    """Publish data to channel

    Data will be converted to bytearray before pushed to memory

    Keyword arguments:
    channel_name -- The name of the channel to publish to
    data -- Data to be published to shared memory
    """
    pickled_data = Pickler(data)
    data_size = sizeof(pickled_data)
    register_to_produce_data(channel_name, data_size)
    cython_publish_data(channel_name, data_size, pickled_data)


def depublish(channel_name):

    cython_depublish(channel_name)


cdef cython_publish_data(channel_name, pickled_data, data_size):
 
    cdef int c_data_size = <int>data_size
    cdef int c_pickled_data = <int> malloc(c_data_size * sizeof(int))

    for i in range(data_size):
        c_pickled_data[i] = <int>(pickled_data[i])

    cdef int *source_ptr = &c_pickled_data
    cdef int c_channel_name = <int>channel_name

    publish_data(c_channel_name, c_data_size, source_ptr)


cdef cython_depublish(channel_name):

    cdef int c_channel_name = <int>channel_name

    deregister_to_produce_data(c_channel_name)

