# distutils: sources = producer.c relay.c
# distutils: include_dirs = Python.h
from pickle import Pickler, Unpickler
from cpython.ref cimport PyObject
from libc.string cimport strcpy
from libc.stdlib cimport malloc


cdef extern register_to_produce_data(int channel_name, int data_size)
cdef extern publish_data(int channel_name, int data_size, int *source_ptr)
cdef extern deregister_to_produce_data(int channel_name)
cdef extern register_to_produce_data(char channelName, int dataSize)
cdef extern publish_data(char channelName, int dataSize, int *sourcePtr)
cdef extern deregister_to_produce_data(char channelName)


def publish(channelName, data):

    """
    Register with relay to produce data... Relay assigns a pointer to shared memory for it to publish to

    Channel name and data pointer location is stored in hash table by relay, where it can be accessed later by both consumers and producers

    Keyword arguments:
    channel_name -- The name of the channel to publish to (need to coordinate with consumers to have matching values
    data_size -- Size of the data to be passed to relay
    buffer_size -- Used in conjunction with data_size to determine total size of shared memory to be assigned to this channel
    """


    pickled_data = Pickler(data)

    register_to_produce_data(channelName, find_c_data_size(pickled_data))

    cython_publish_data(channelName, data)


def depublish(channelName):

    cython_depublish(channelName)

cdef find_c_data_size(pickled_data):

    cdef int C_dataSize = <int>(sizeof(pickled_data))

    return C_dataSize

cdef cython_publish_data(channelName, data):

    pickled_data = Pickler(data)

    cdef int C_dataSize = find_c_data_size(pickled_data)

    """

    cdef int C_pickled_data = <int> malloc(C_dataSize * sizeof(int))

    for i in range(dataSize):

        C_pickled_data[i] = <int>(pickled_data[i])

    cdef int *sourcePtr = &C_pickled_data

    """

    cdef void *voidSourcePtr = <void*>pickled_data

    cdef int *sourcePtr = <int*>voidSourcePtr

    cdef char C_channelName = <char>channelName

cdef cython_depublish(channel_name):


cdef cython_depublish(channelName):

    cdef char C_channelName = <char>channelName

    deregister_to_produce_data(C_channelName)

