from threading import Thread
from time import sleep

from src.airmar.config_reader import read_pin_config, read_interval
from src.airmar.airmar_receiver import AirmarReceiver


class AirmarInputThread(Thread):
    def __init__(self, mock_bbio=None):
        super().__init__()

        # TODO: Move params to config if this is actually used
        port = serial.Serial(port="/dev/tty01", baudrate=4800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial)

        self.receiver = AirmarReceiver(read_pin_config(mock_bbio=mock_bbio), port)

        self.keep_reading = True
        self.read_interval = read_interval()


    def run(self):
        self.receiver.start()
        while self.keep_reading:
            self.receiver.send_data()
            sleep(self.read_interval)
