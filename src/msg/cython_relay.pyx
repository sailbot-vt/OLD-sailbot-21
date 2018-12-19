from threading import Thread

cdef extern from "relay.h":
    ctypedef struct Relay:
        pass
    Relay* init_relay()


cdef class RelayWrapper:
    """Python wrapper for a Relay*"""
    cdef Relay* relay

    def __cinit__(self):
        self.relay = init_relay()


class MsgThread(Thread):
    """Holds the msg relay state in a separate thread"""

    def __init__(self):
        super().__init__()
        self.relay = RelayWrapper()

    def run(self):
        while True:
            pass

    def get_relay(self):
        return self.relay
