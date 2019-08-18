from threading import Thread
from time import sleep

from src.rc_input.config_reader import read_pin_config, read_interval
from src.rc_input.rc_receiver import RCReceiver


class RCInputThread(Thread):
    """A separate thread to manage reading the RC inputs and broadcasting the data to the system.

    Should accept multiple boat configurations, and should be general enough to allow for easy extension.
    """
    def __init__(self, mock_bbio=None):
        """Builds a new RC input thread."""
        super().__init__()

        self.receiver = RCReceiver(read_pin_config(mock_bbio=mock_bbio))

        self.keep_reading = True
        self.read_interval = read_interval()

    def run(self):
        """Starts a regular input read interval."""
        while True:
            self.receiver.send_inputs()
            sleep(self.read_interval)
