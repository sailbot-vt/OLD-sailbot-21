import math


class AirmarProcessor:
    """Defines an airmar data processor that stores airmar data given a NMEASentence object"""

    def __init__(self, broadcaster):
        """Initializes a new airmar data processor.

        Returns:
        A new AirmarProcessor
        """
        self.broadcaster = broadcaster
        self.wind_data = {
            "WIND_SPEED": None,
            # wind heading in degrees
            "WIND_HEADING": None,
        }

    def update_airmar_data(self, nmea):
        """ Updates the wind and boat data in the broadcaster given a NMEASentence object

        Keyword arguments:
        nmea -- a NMEASentence object containing wind and boat data.
        """
        self._update_wind_data(nmea=nmea)
        self._update_boat_data(nmea=nmea)

    ### --- WIND UPDATES --- ###

    def _update_wind_data(self, nmea):
        """ Updates the current and average wind speed and heading if availible.

        Keyword arguments:
        nmea -- a NMEASentence object containing wind_speed_meters
            and direction_true

        Side Effects:
        Sends wind data to the airmar broadcaster.
        """
        if nmea.wind_speed_meters is not None and nmea.direction_true is not None:
            wind_speed = float(nmea.wind_speed_meters)
            wind_head = float(nmea.wind_direction_true)

            self._update_wind_averages(
                wind_speed=wind_speed, wind_angle=wind_head)

    def _update_wind_averages(self, wind_speed, wind_angle):
        """ Calculates and writes to the ship data the average wind speed and heading.

        Keyword arguments:
        airmar_data -- the 'old' wind speed and direction averages
        wind_speed -- the current wind speed read in meters.
        wind_direc -- the current wind heading read in degrees.

        Side Effects:
        Updates wind data dictionary in processor.
        Sends wind data to the airmar broadcaster.
        """
        wind_angle = math.radians(wind_angle)
        wind_angle_old = math.radians(self.wind_data["WIND_HEADING"])

        wind_speed_old = self.wind_data["WIND_SPEED"]

        # calculate components
        old_x = wind_speed_old * math.cos(wind_angle_old)
        old_y = wind_speed_old * math.sin(wind_angle_old)

        new_x = wind_speed * math.cos(wind_angle)
        new_y = wind_speed * math.sin(wind_angle)

        # Weighted values
        weight = 0.3         # working constant from old code
        x = old_x * (1 - weight) + new_x * (weight)
        y = old_y * (1 - weight) + new_y * (weight)

        speed = math.sqrt(x*x + y*y)
        heading = math.degrees(math.atan2(x, y)) % 360

        # Updates dictionary
        self.wind_data["WIND_SPEED"] = speed
        self.wind_data["WIND_HEADING"] = heading
        self.broadcaster.read_wind_speed(wind_speed=speed)
        self.broadcaster.read_wind_heading(wind_heading=heading)

    ### --- BOAT UPDATES ---- ###

    def _update_boat_data(self, nmea):
        """ Updates the boat's latitude, longitude, heading and speed

        Keyword arguments:
        nmea -- a NMEASentence object containing 'latitude', 'longitude', 'heading', and 'speed'

        Side Effects:
        Updates wind data dictionary in processor.
        Sends boat data to the airmar broadcaster.
        """
        self._update_boat_lat(nmea=nmea)
        self._update_boat_long(nmea=nmea)
        self._update_boat_head(nmea=nmea)
        self._update_boat_speed(nmea=nmea)

    def _update_boat_lat(self, nmea):
        """ Updates the boat's latitude. Only accepts values > 10.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'latitude'

        Side Effects:
        Sends boat data to the airmar broadcaster.
        """
        if nmea.latitude is not None and float(nmea.latitude) > 10:
            boat_lat = float(nmea.latitude)
            self.broadcaster.read_boat_latitude(boat_lat=boat_lat)

    def _update_boat_long(self, nmea):
        """ Updates the boat's longitude. Only accepts values < -10

        Keyword arguments:
        nmea -- a NMEASentence object containing 'longitude'

        Side Effects:
        Sends boat data to the airmar broadcaster
        """
        if nmea.longitude is not None and float(nmea.longitude) < -10:
            boat_long = float(nmea.longitude)
            self.broadcaster.read_boat_longitude(boat_long=boat_long)

    def _update_boat_head(self, nmea):
        """ Updates the boat's heading.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'heading'

        Side Effects:
        Sends boat data to the airmar broadcaster
        """
        if nmea.heading is not None:
            boat_head = float(nmea.heading) % 360
            self.broadcaster.read_boat_heading(boat_head=boat_head)

    def _update_boat_speed(self, nmea):
        """ Updates the boat's speed.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'speed'

        Side Effects:
        Sends boat data to the airmar broadcaster
        """
        if nmea.speed is not None:
            boat_speed = float(nmea.speed)
            self.broadcaster.read_boat_speed(boat_speed=boat_speed)
