from threading import Thread
from time import sleep

from src.airmar.config_reader import read_pin_config, read_interval, read_port_config
from src.airmar.airmar_receiver import AirmarReceiver
from src.airmar.airmar_broadcaster import make_broadcaster, AirmarBroadcasterType


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""

    def __init__(self, mock_bbio=None, mock_port=None, broadcaster_type=None):
        """Builds a new airmar input thread."""
        super().__init__()

        self.broadcaster = make_broadcaster(broadcaster_type=broadcaster_type)
        self.pin = read_pin_config(mock_bbio=mock_bbio)
        self.port = read_port_config(mock_port=mock_port)

        self.receiver = AirmarReceiver(
            broadcaster=self.broadcaster, pin=self.pin, port=self.port)

        self.keep_reading = True
        self.read_interval = read_interval()

    def run(self):
        """Starts a regular read interval."""
        self.receiver.start()
        while self.keep_reading:
            self.receiver.send_airmar_data()
            sleep(self.read_interval)
        self.receiver.stop()
