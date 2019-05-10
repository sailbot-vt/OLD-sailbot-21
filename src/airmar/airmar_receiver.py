from src.airmar.airmar_processor import AirmarProcessor
from src.airmar.nmeaparser.nmeaparser import NmeaParser


class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""

    def __init__(self, broadcaster, ids, pin, port):
        """Initializes a new airmar receiver.

        Keyword arguments:
        pin -- The UART pin object

        Returns:
        A new Airmar Receiver
        """
        self.parser = NmeaParser()
        self.ids = ids
        self.is_running = False
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor(broadcaster=broadcaster)

    def start(self):
        """ Sets up uart pin and open port to start listening. 
        Enables sentences specified by ids field to airmar serial port."""
        self.uart_pin.setup()
        # Close port before open needed.
        self.port.close()
        self.port.open()
        # Resumes sentence transmition
        # TODO encoding variable to field
        self.port.write(
            "{}".format(self.parser.power(resume=1)).encode(self.port.encoding))
        # Disable all sentence transmitions first.
        self.port.write(
            "{}".format(self.parser.toggle(enable=0)).encode(self.port.encoding))
        for sid in self.ids:
            # Enables sentences specified by config
            self.port.write(
                "{}".format(self.parser.toggle(sid)).encode(self.port.encoding))
        self.is_running = True

    def send_airmar_data(self):
        """ Sends nmea sentence from serial port to processor to broadcast data """
        data = self.parser.parse(self.port.read_line(terminator='\r\n'))
        # sentence type can be determined by first element of data.
        if data is not None:
            self.processor.update_airmar_data(nmea=data)

    def stop(self):
        """ Stops the pin and port """
        # Suspends sentences.
        self.port.write(
            "{}".format(self.parser.power(resume=0)).encode(self.port.encoding))
        self.port.close()
        self.uart_pin.cleanup()
        self.is_running = False
