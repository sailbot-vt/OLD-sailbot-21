import pynmea2

class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""
    def __init__(self, broadcaster, pin, port):
        """Initializes a new airmar receiver.

        Keyword arguments:
        pin -- The UART pin object

        Returns:
        A new Airmar Receiver
        """
        self.broadcaster = broadcaster
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor()


    def start(self):
        """ Sets up uart pin and open serial port to start listening."""
        self.uart_pin.setup()
        self.port.open()

    def send_ship_data(self):
        """Sends ship data to the broadcaster to be published.

        Preconditions:
        ship_data dictionary must include keys:
            'WIND_SPEED_AVERAGE'
            'WIND_HEADING_AVERAGE'
            'BOAT_LATITUDE'
            'BOAT_LONGITUDE'
            'BOAT_HEADING'
            'BOAT_SPEED'

        Side effects:
        Updates ship data dictionary
        Does not broadcast if value in dictionary is None
        """
        self._update_ship_data()
        data = self.processor.get_data()
        self.broadcaster.read_wind_speed(wind_speed=data["WIND_SPEED_AVERAGE"])
        self.broadcaster.read_wind_heading(wind_head=data["WIND_HEADING_AVERAGE"])
        self.broadcaster.read_boat_latitude(boat_lat=data["BOAT_LATITUDE"])
        self.broadcaster.read_boat_longitude(boat_long=data["BOAT_LONGITUDE"])
        self.broadcaster.read_boat_heading(boat_head=data["BOAT_HEADING"])
        self.broadcaster.read_boat_speed(boat_speed=data["BOAT_SPEED"])

    def _update_ship_data(self):
        """ Sends NMEASentence object to airmar processor to update ship data."""
        nmea_obj = self._parse_msg()
        if nmea_obj is not None:
            self.processor.update_data(data=nmea_obj)

    def _parse_msg(self):
        """ Reads NMEA0183 message from serial port.

        Returns:
        A NMEASentence object containing ship data.
        """
        raw_msg = self._read_raw_msg()
        cleaned_msg = self._clean_raw_msg(raw_msg=raw_msg)

        if cleaned_msg is None:
            return None
        return pynmea2.parse(cleaned_msg)

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

    def _clean_raw_msg(self, raw_msg):
        """ Cleans the raw message from serial port.

        Keyword arguments:
        raw_message -- The raw bytes read from serial port.

        Returns:
        The cleaned sentence in NMEA 0183.
        """
        # TODO: regex way to do this.
        # Note: nmea0183 sentences starts with $ or ! and
        # ends in <CR><LF> (hex:0x0d, dec:13)(hex:0x0d, dec:13)
        cleaned_msg = ""
        if len(cleaned_msg) < 2:
            return None
        return cleaned_msg

    def stop():
        """ Stops the pin

        WARNING: According to lib docs, causes kernal panic.
        """
        self.uart_pin.cleanup()
