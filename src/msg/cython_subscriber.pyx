# distutils: sources = subscriber.c

from cpython.ref cimport PyObject


cimport cython_subscriber

cdef class _Subscriber:
    cdef cython_subscriber.Subscriber* subscriber

    def __cinit__(self):
        self.subscriber = NULL

    def subscribe(self, channel_name, data_callback):
        """Subscribe to an event channel.

        Keyword arguments:
        channel_name -- The name of the channel to subscribe to.
        data_callback -- Function to execute on event, passed data from publisher
        """
        self.subscriber = cython_subscriber.subscribe(channel_name, <PyObject*>data_callback)

    def __dealloc__(self):
        cdef cython_subscriber.Subscriber* temp = <Subscriber*>self.subscriber
        cython_subscriber.unsubscribe(&temp)
