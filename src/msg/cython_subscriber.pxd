from cpython.ref cimport PyObject

cdef extern from "subscriber.h":
    ctypedef struct Subscriber:
        pass
    ctypedef struct Relay:
        pass
    Subscriber* subscribe(Relay* relay, char* channel_name, PyObject* callback)
    void unsubscribe(Relay* relay, Subscriber **subscriber)