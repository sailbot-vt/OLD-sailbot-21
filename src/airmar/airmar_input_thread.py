from threading import Thread
from time import sleep

from src.airmar.config_reader import read_pin_config, read_interval, read_port_config, read_sentences
from src.airmar.airmar_receiver import AirmarReceiver
from src.airmar.airmar_broadcaster import make_broadcaster, AirmarBroadcasterType


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""

    def __init__(self, mock_bbio=None, mock_port=None, broadcaster_type=None):
        """Builds a new airmar input thread."""
        super().__init__()
        if broadcaster_type is None:
            # Default broadcaster:
            broadcaster_type = AirmarBroadcasterType.Messenger

        broadcaster = make_broadcaster(broadcaster_type=broadcaster_type)
        pin = read_pin_config(mock_bbio=mock_bbio)
        port = read_port_config(mock_port=mock_port)
        sentences = read_sentences()

        self.receiver = AirmarReceiver(
            broadcaster=broadcaster, sentences=sentences, pin=pin, port=port)

        self.keep_reading = True
        self.read_interval = read_interval()

    def run(self):
        """Starts a regular read interval.

        Side effects:
        -- self.keep_reading : True, receiver start, if not started/stopped
        -- self.keep_reading : False, receiver stop
        """
        self.keep_reading = True
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
