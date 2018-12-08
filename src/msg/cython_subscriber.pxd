from cpython.ref cimport PyObject

cdef extern from "subscriber.h":
    ctypedef struct Subscriber:
        pass
    Subscriber* subscribe(char* channel_name, PyObject* callback)
    void unsubscribe(Subscriber **subscriber)