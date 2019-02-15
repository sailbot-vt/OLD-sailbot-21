from threading import Thread
from time import sleep

from src.airmar.config_reader import read_pin_config, read_interval
from src.airmar.airmar_receiver import AirmarReceiver


class AirmarInputThread(Thread):
    """A separate thread to manage reading the airmar inputs."""
    def __init__(self, mock_bbio=None):
        """Builds a new airmar input thread."""
        super().__init__()

        # TODO: Move params to config if this is actually used
        # Serial port used to read nmea sentences
        port = serial.Serial(port="/dev/tty01", baudrate=4800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial)

        self.receiver = AirmarReceiver(read_pin_config(mock_bbio=mock_bbio), port)

        self.keep_reading = True
        self.read_interval = read_interval()


    def run(self):
        """Starts a regular read interval."""
        self.receiver.start()
        while self.keep_reading:
            self.receiver.send_data()
            sleep(self.read_interval)
