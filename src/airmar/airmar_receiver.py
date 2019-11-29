from src.airmar.airmar_processor import AirmarProcessor
from src.airmar.config_reader import read_pin_config, read_port_config, read_ids
from src.airmar.nmeaparser.nmea_parser import NmeaParser

from threading import Lock

mutex = Lock()

class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""

    def __init__(self, broadcaster, mock_bbio=None, mock_port=None):
        """Initializes a new airmar receiver.

        Keyword arguments:
        pin -- The UART pin object

        Returns:
        A new Airmar Receiver
        """
        self.parser = NmeaParser()
        self.ids = read_ids()
        self.is_running = False
        self.uart_pin = read_pin_config(mock_bbio=mock_bbio)
        self.port = read_port_config(mock_port=mock_port)
        self.processor = AirmarProcessor(
            broadcaster=broadcaster, parser=self.parser)

    def start(self):
        """ Sets up uart pin and open port to start listening. 
        Enables sentences specified by ids field to airmar serial port."""
        # Setup port/pin
        self.uart_pin.setup()
        self.port.open()

        # Airmar specific sentence transmissions to airmar port.
        # Resumes sentence transmission
        self.port.write(
            "{}".format(self.parser.power(resume=1)).encode(self.port.encoding))
        
        # First, disable all transmissions
        self.port.write(
            "{}".format(self.parser.toggle(enable=0)).encode(self.port.encoding))
        toggles = self.parser.toggle(self.ids)
        for toggle in toggles:
            # Second, enable specified transmissions in config
            self.port.write("{}".format(toggle).encode(self.port.encoding))
        
        self.is_running = True

    def send_airmar_data(self):
        """ Sends nmea sentence from serial port to processor to broadcast data """
        sentence = self.port.read_line(terminator='\r\n')
        data = self.parser.parse(sentence)
        if data is not None:
            mutex.acquire()
            self.processor.update_airmar_data(nmea=data)
            mutex.release()

    def stop(self):
        """ Stops the pin and port """
        # Suspends sentences.
        self.port.write(
            "{}".format(self.parser.power(resume=0)).encode(self.port.encoding))
       
        # cleanup and close ports and pins
        self.port.close()
        self.uart_pin.cleanup()
        self.is_running = False
