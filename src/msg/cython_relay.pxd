from libc.stdint cimport uintptr_t


cdef extern from "relay.h":
    ctypedef struct Relay:
        pass
    Relay* init_relay()
    void destroy_relay(Relay** relay)


cdef class RelayWrapper:
    cdef uintptr_t relay
    cpdef uintptr_t get_relay(self)
