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
        if broadcaster_type is None:
            # Default broadcaster:
            broadcaster_type = AirmarBroadcasterType.Messenger

        self.broadcaster = make_broadcaster(broadcaster_type=broadcaster_type)
        self.pins = read_pin_config(mock_bbio=mock_bbio)
        self.ports = read_port_config(mock_port=mock_port)

        self.receivers = {
            "WIND": AirmarReceiver(
            broadcaster=self.broadcaster, pin=self.pins["WIND"], port=self.ports["WIND"]),
            "BOAT": AirmarReceiver(
            broadcaster=self.broadcaster, pin=self.pins["BOAT"], port=self.ports["BOAT"])
        }

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
            for receiver in self.receivers.values():
                if not receiver.is_running:
                    receiver.start()
                receiver.send_airmar_data()
                sleep(read_interval)
        else:
            for receiver in self.receivers.values():
                receiver.stop()

    def stop(self):
        """ Pauses current thread without killing it. """
        self.keep_reading = False
