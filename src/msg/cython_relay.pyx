from libc.stdint cimport uintptr_t


cimport src.msg.cython_relay


cdef class RelayWrapper:
    """Python wrapper for a Relay*"""
    def __cinit__(self):
        self.relay = <uintptr_t>init_relay()

    cpdef uintptr_t get_relay(self):
        return self.relay

    def __dealloc__(self):
        cdef Relay* relay = <Relay*>self.relay
        destroy_relay(&relay)
