from threading import Thread
from time import sleep

import serial

from src.airmar.config_reader import read_pin_config, read_interval, read_port_config
from src.airmar.airmar_receiver import AirmarReceiver
from src.airmar.airmar_broadcaster import make_broadcaster, AirmarBroadcasterType


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""

    def __init__(self, mock_bbio=None):
        """Builds a new airmar input thread."""
        super().__init__()

        self.broadcaster = make_broadcaster(AirmarBroadcasterType.Messenger)

        # TODO: Move params to config if this is actually used
        # Serial port used to read nmea sentences
        # Might have to do port=`ls /dev/serial/by-id/`
        self.port = serial.Serial(port="/dev/tty01", baudrate=4800, timeout=0)
        # parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,

        self.receiver = AirmarReceiver(broadcaster=self.broadcaster, pin=read_pin_config(
            mock_bbio=mock_bbio), port=self.port)

        self.keep_reading = True
        self.read_interval = read_interval()

    def run(self):
        """Starts a regular read interval."""
        self.receiver.start()
        while self.keep_reading:
            self.receiver.send_airmar_data()
            sleep(self.read_interval)
