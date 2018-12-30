from threading import Thread
from src.msg.cython_relay import RelayWrapper


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
