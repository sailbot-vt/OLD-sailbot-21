from threading import Thread
from time import sleep

from src.airmar.config_reader import read_pin_config, read_interval, read_port_config, read_ids
from src.airmar.airmar_receiver import AirmarReceiver
from src.broadcaster.broadcaster import make_broadcaster, BroadcasterType


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""

    def __init__(self, mock_bbio=None, mock_port=None, broadcaster_type=None):
        """Builds a new airmar input thread."""
        super().__init__()

        if broadcaster_type is None:
            broadcaster_type = BroadcasterType.Messenger
        self.broadcaster = make_broadcaster(broadcaster_type=broadcaster_type)
        
        pin = read_pin_config(mock_bbio=mock_bbio)
        port = read_port_config(mock_port=mock_port)
        ids = read_ids()

        self.receiver = AirmarReceiver(
            broadcaster=self.broadcaster, ids=ids, pin=pin, port=port)

        self.keep_reading = True
        self.read_interval = read_interval()

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
            self.receiver.send_airmar_data()
            sleep(self.read_interval)
        else:
            self.receiver.stop()

    def stop(self):
        """ Pauses current thread without killing it. """
        self.keep_reading = False
