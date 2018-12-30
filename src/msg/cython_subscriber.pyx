from cpython.ref cimport PyObject

cdef extern from "subscriber.h":
    ctypedef struct Subscriber:
        pass
    ctypedef struct Relay:
        pass
    Subscriber* subscribe(Relay* relay, char* channel_name, PyObject* callback)
    void unsubscribe(Relay* relay, Subscriber *subscriber)


cdef class _Subscriber:
    cdef Subscriber* subscriber
    cdef Relay* relay

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
        self.subscriber = subscribe(self.relay, channel_name, <PyObject*>data_callback)

    def __dealloc__(self):
        cdef Subscriber* temp = <Subscriber*>self.subscriber
        unsubscribe(self.relay, temp)
