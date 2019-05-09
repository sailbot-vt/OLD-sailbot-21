import re

from src.airmar.airmar_processor import AirmarProcessor


class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""

    def __init__(self, broadcaster, sentences, pin, port):
        """Initializes a new airmar receiver.

        Keyword arguments:
        pin -- The UART pin object

        Returns:
        A new Airmar Receiver
        """
        self.sentences = sentences
        self.is_running = False
        self.remaining_input = ""
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor(broadcaster=broadcaster)

    def start(self):
        """ Sets up uart pin and open port to start listening."""
        self.uart_pin.setup()
        self.port.open()
        self.port.write(b"$PAMTC,EN,ALL,0,1,,*00\r\n")
        # TODO Need to implement check sum
        for sentence_id in self.sentences:
            sentence = b"{}".format(sentence_id)
            self.port.write(sentence)
        self.is_running = True

    def send_airmar_data(self):
        """ Sends NMEASentence object to airmar processor to broadcast airmar data."""
        nmea_obj = self._parse_msg()

        if nmea_obj is not None:
            self.processor.update_airmar_data(nmea=nmea_obj)

    def stop(self):
        """ Stops the pin and port """
        self.port.close()
        self.uart_pin.cleanup()
        self.is_running = False
