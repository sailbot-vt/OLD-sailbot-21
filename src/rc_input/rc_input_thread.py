from threading import Thread
from time import sleep

from src.rc_input.pin_config_reader import read_pin_config
from src.rc_input.rc_receiver import RCReceiver
from src.rc_input.rc_broadcaster import make_broadcaster, RCInputBroadcasterType

RC_READ_INTERVAL = 50 / 1000  # 50 milliseconds


class RCInputThread(Thread):
    """A separate thread to manage reading the RC inputs and broadcasting the data to the system.

    Should accept multiple boat configurations, and should be general enough to allow for easy extension.
    """
    def __init__(self, config=None):
        """Builds a new RC input thread."""
        super().__init__()

        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Messenger)
        self.receiver = RCReceiver(broadcaster=self.broadcaster, pins=read_pin_config())

        self.keep_reading = True

    def run(self):
        """Starts a regular input read interval."""
        while True:
            self.receiver.read_input()
            sleep(RC_READ_INTERVAL)
