import pynmea2

class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""
    def __init__(self, pin, port):
        """Initializes a new airmar receiver.

        Keyword arguments:
        pin -- The UART pin object

        Returns:
        A new Airmar Receiver
        """
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor()

    def start(self):
        """ Sets up uart pin and open serial port to start listening."""
        self.uart_pin.setup()
        self.port.open()

    def send_data(self):
        """ Sends pynmea2 object to airmar processor to store ship data."""
        # PyPubsub or keep as a dict?
        msg = self._read_msg()
        if msg is not None:
            data = pynmea2.parse(msg)
            self.processor.update_data(data=data)

    def _read_msg(self):
        """ Reads NMEA0183 message from serial port.

        Returns:
        NMEA 0183 message as a string
        """
        raw_msg = self._read_raw_data()
        msg = self._sanitized_data(raw_msg=raw_msg)
        return msg

    def _read_raw_msg(self):
        """ Reads in the bytes from the serial port.

        Returns:
        The raw sentence read in from the serial port.
        """
        try:
            bytes = self.port.inWaiting()
        except:
            bytes = 0
        raw_msg = self.port.read(size=bytes)
        return raw_msg

    def _parse_msg(self, raw_msg):
        """ Parses the NMEA 0183 message.

        Keyword arguments:
        raw_message -- The raw bytes read from serial port.

        Returns:
        The parsed sentence.
        """
        # TODO: regex way to do this.
        # Note: nmea0183 sentences starts with $ or ! and
        # ends in <CR><LF> (hex:0x0d, dec:13)(hex:0x0d, dec:13)
        parsed_msg = ""
        if len(parsed_msg) < 2:
            return None
        return parsed_msg

    def stop():
        """ Stops the pin

        WARNING: According to lib docs, causes kernal panic.
        """
        self.uart_pin.cleanup()
