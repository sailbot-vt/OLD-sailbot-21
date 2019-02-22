import pynmea2

from src.airmar.airmar_processor import AirmarProcessor


class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""

    def __init__(self, broadcaster, pin, port):
        """Initializes a new airmar receiver.

        Keyword arguments:
        pin -- The UART pin object

        Returns:
        A new Airmar Receiver
        """
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor(broadcaster=broadcaster)

    def start(self):
        """ Sets up uart pin and open port to start listening."""
        self.uart_pin.setup()
        self.port.open()

    def send_airmar_data(self):
        """ Sends NMEASentence object to airmar processor to broadcast airmar data."""
        nmea_obj = self._parse_msg()
        if nmea_obj is not None:
            self.processor.update_airmar_data(nmea=nmea_obj)

    def _parse_msg(self):
        """ Reads NMEA0183 message from serial port.

        Returns:
        A NMEASentence object containing ship data.
        None if a message could not be processed correctly.
        """
        msg = self.port.read()

        try:
            nmea = pynmea2.parse(msg)
        except Exception:
            # TODO log error.
            return None
        return nmea

    def stop(self):
        """ Stops the pin """
        self.port.close()
        self.uart_pin.cleanup()
