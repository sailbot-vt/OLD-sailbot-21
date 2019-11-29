from threading import Thread
from time import sleep

from src.airmar.airmar_receiver import AirmarReceiver
from src.airmar.config_reader import read_interval
from src.broadcaster.broadcaster import make_broadcaster, BroadcasterType


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""

    def __init__(self, mock_bbio=None, mock_port=None, broadcaster_type=None, filename=None):
        """Builds a new airmar input thread."""
        super().__init__()

        # Make broadcaster
        if broadcaster_type is None:
            # pubsub by default
            broadcaster_type = BroadcasterType.Messenger

        # broadcaster as public attribute
        self.broadcaster = make_broadcaster(
            broadcaster_type=broadcaster_type, filename=filename)
        
        # make receiver
        self.receiver = AirmarReceiver(
                broadcaster=self.broadcaster, mock_bbio=mock_bbio, mock_port=mock_port)

        self.keep_reading = True
        self.read_interval = read_interval()
        print("Airmar ready\n")

    def run(self):
        """Starts a regular read interval.
        Side effects:
        -- self.keep_reading : True, receiver start, if not started/stopped
        -- self.keep_reading : False, receiver stop
        """
        self.keep_reading = True
        while self.keep_reading:
            if not self.receiver.is_running:
                self.receiver.start()
            try:
                self.receiver.send_airmar_data()
            except:
                continue
            sleep(self.read_interval)
        else:
            self.receiver.stop()

    def stop(self):
        """ Pauses current thread without killing it. """
        self.keep_reading = False
