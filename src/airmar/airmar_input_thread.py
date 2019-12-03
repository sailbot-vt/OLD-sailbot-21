from threading import Thread
from time import sleep

from src.airmar.airmar_receiver import AirmarReceiver
from src.airmar.config_reader import read_interval
from src.broadcaster.broadcaster import make_broadcaster, BroadcasterType


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""

    def __init__(self, logger, mock_bbio=None, mock_port=None, 
        broadcaster_type=BroadcasterType.Messenger,
        filename=None):
        """Builds a new airmar input thread."""
        super().__init__()

        # broadcaster as public attribute
        self.broadcaster = make_broadcaster(
            broadcaster_type=broadcaster_type, filename=filename)
        
        # make receiver
        self.receiver = AirmarReceiver(logger=logger,
                broadcaster=self.broadcaster, 
                mock_bbio=mock_bbio, mock_port=mock_port)

        self.read_interval = read_interval()

    def run(self):
        """Starts a regular read interval."""
        while self.is_alive():
            if not self.receiver.is_running:
                self.receiver.start()
                self.receiver.send_airmar_data()
            sleep(self.read_interval)
        else:
            # cleanup on thread exit.
            self.receiver.stop()