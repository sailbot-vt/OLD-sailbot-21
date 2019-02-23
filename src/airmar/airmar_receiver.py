import pynmea2
import re

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
        self.is_running = False
        self.stored_data = ""
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor(broadcaster=broadcaster)

    def start(self):
        """ Sets up uart pin and open port to start listening."""
        self.uart_pin.setup()
        self.port.open()
        self.is_running = True

    def send_airmar_data(self):
        """ Sends NMEASentence object to airmar processor to broadcast airmar data."""
        nmea_obj = self._parse_msg()

        if nmea_obj is not None:
            self.processor.update_airmar_data(nmea=nmea_obj)

    def _parse_msg(self):
        """ Parses the NMEA sentence received from serial port.

        Returns:
        A NMEASentence object containing ship data.
        None if a message could not be processed correctly.
        """
        msg = self._read_msg()

        try:
            nmea = pynmea2.parse(msg)
        except Exception:
            # TODO log error.
            return None
        return nmea

    def _read_msg(self):
        """ Reads a full NMEA0183 sentence from the port.

        Returns:
        A string in NMEA1083 containing ship or wind data.
        """
        line = ""
        while self.port.is_open():
            if self.stored_data:
                line = self.stored_data
                self.stored_data = ""

            port_buffer = self.port.read()
            if port_buffer:
                line = line + port_buffer

            if re.search("\r\n", line):
                data, self.stored_data = line.split("\r\n")
                line = ""
                return data
        return line

    def stop(self):
        """ Stops the pin and port """
        self.port.close()
        self.uart_pin.cleanup()
        self.is_running = False
