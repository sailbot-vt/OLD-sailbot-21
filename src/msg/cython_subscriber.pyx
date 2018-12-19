from cpython.ref cimport PyObject


cimport cython_subscriber


cdef class _Subscriber:
    cdef cython_subscriber.Subscriber* subscriber
    cdef cython_subscriber.Relay* relay

    def __cinit__(self):
        self.subscriber = NULL
        self.relay = NULL

    def subscribe(self, relay, channel_name, data_callback):
        """Subscribe to an event channel.

        Keyword arguments:
        relay -- The relay to which to subscribe.
        channel_name -- The name of the channel to subscribe to.
        data_callback -- Function to execute on event, passed data from publisher
        """
        self.relay = <Relay*>relay.relay
        self.subscriber = cython_subscriber.subscribe(self.relay, channel_name, <PyObject*>data_callback)

    def __dealloc__(self):
        cdef cython_subscriber.Subscriber* temp = <Subscriber*>self.subscriber
        cython_subscriber.unsubscribe(self.relay, &temp)
