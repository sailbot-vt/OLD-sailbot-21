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
        self.broadcaster = broadcaster
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor()

    def start(self):
        """ Sets up uart pin and open port to start listening."""
        self.uart_pin.setup()
        self.port.open()

    def send_airmar_data(self):
        """Sends airmar data to the broadcaster to be published.

        Preconditions:
        ship_data dictionary must include keys:
            'WIND_SPEED_AVERAGE'
            'WIND_HEADING_AVERAGE'
            'BOAT_LATITUDE'
            'BOAT_LONGITUDE'
            'BOAT_HEADING'
            'BOAT_SPEED'

        Side effects:
        Updates airmar_data dictionary in AirmarProcessor
        Does not broadcast if value in dictionary is None
        """
        self._update_airmar_data()
        data = self.processor.get_airmar_data()
        self.broadcaster.read_wind_speed(wind_speed=data["WIND_SPEED_AVERAGE"])
        self.broadcaster.read_wind_heading(
            wind_head=data["WIND_HEADING_AVERAGE"])
        self.broadcaster.read_boat_latitude(boat_lat=data["BOAT_LATITUDE"])
        self.broadcaster.read_boat_longitude(boat_long=data["BOAT_LONGITUDE"])
        self.broadcaster.read_boat_heading(boat_head=data["BOAT_HEADING"])
        self.broadcaster.read_boat_speed(boat_speed=data["BOAT_SPEED"])

    def _update_airmar_data(self):
        """ Sends NMEASentence object to airmar processor to update airmar data."""
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

        if msg is None:
            return None
        try:
            nmea = pynmea2.parse(msg)
        except Exception:
            # TODO log error.
            return None
        return nmea

    def stop(self):
        """ Stops the pin

        WARNING: According to lib docs, causes kernal panic.
        """
        self.uart_pin.cleanup()
