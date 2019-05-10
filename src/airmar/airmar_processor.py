import math


class AirmarProcessor:
    """ Defines an airmar data processor that stores airmar data given a NMEASentence object

    Note: Can only process $GPVTG, $GPGGA, and $WIMWD NMEA0183 sentences.

    TODO Update this processor to make it less hardcoded: placing sentence parsers in nmeaparser package
    """

    def __init__(self, broadcaster):
        """ Initializes a new airmar data processor.

        Returns:
        A new AirmarProcessor
        """
        self.nmea_contents = None
        self.broadcaster = broadcaster
        self.wind_data = {
            "WIND_SPEED": None,
            # wind heading in degrees
            "WIND_HEADING": None,
        }

    def update_airmar_data(self, nmea):
        """ Updates the wind and boat data in the broadcaster given a NMEASentence object

        Precondition: NMEA0183 sentences must be: $GPVTG $GPGGA or $WIMWD

        Keyword arguments:
        nmea -- a NMEASentence object containing wind and boat data.
        """
        self.nmea_contents = None
        self.nmea_contents = self._read_nmea_contents(nmea)
        if "Wind direction true" in self.nmea_contents and "wind_speed_meters" in self.nmea_contents:
            self._update_wind_data(nmea=nmea)
        self._update_boat_data(nmea=nmea)

    def _read_nmea_contents(self, nmea):
        """ Create list of attributes that nmea sentence has for quick checks. 

        Keyword arguments:
        nmea -- a NMEASentence object containing wind and boat data.

        Returns:
        A list of nmea attributes in the NMEASentence object
        """
        return [field for tup in nmea.fields for field in tup]

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
            wind_head = float(nmea.direction_true)

            # First measurements
            if self.wind_data["WIND_HEADING"] is None:
                self.wind_data["WIND_HEADING"] = wind_head
            if self.wind_data["WIND_SPEED"] is None:
                self.wind_data["WIND_SPEED"] = wind_speed

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
        old_x = wind_speed_old * math.sin(wind_angle_old)
        old_y = wind_speed_old * math.cos(wind_angle_old)

        new_x = wind_speed * math.sin(wind_angle)
        new_y = wind_speed * math.cos(wind_angle)

        # Weighted values
        weight = 0.3  # Supposedly working weight from old code
        x = old_x * (1 - weight) + new_x * (weight)
        y = old_y * (1 - weight) + new_y * (weight)

        speed = math.sqrt(x*x + y*y)
        heading = math.degrees(math.atan2(x, y)) % 360

        # Updates dictionary
        self.wind_data["WIND_SPEED"] = speed
        self.wind_data["WIND_HEADING"] = heading
        self.broadcaster.read_wind_speed(wind_speed=speed)
        self.broadcaster.read_wind_heading(wind_head=heading)

    ### --- BOAT UPDATES ---- ###

    def _update_boat_data(self, nmea):
        """ Updates the boat's latitude, longitude, heading and speed

        Preconditions:
        nmea_contents field must be updated for current NMEASentence

        Keyword arguments:
        nmea -- a NMEASentence object containing 'latitude', 'longitude', 'heading', and 'speed'

        Side Effects:
        Updates wind data dictionary in processor.
        Sends boat data to the airmar broadcaster.
        """
        if "Latitude" in self.nmea_contents:
            self._update_boat_lat(nmea=nmea)
        if "Longitude" in self.nmea_contents:
            self._update_boat_long(nmea=nmea)
        if "true_track" in self.nmea_contents:
            self._update_boat_head(nmea=nmea)
        if "Speed over ground kmph" in self.nmea_contents:
            self._update_boat_speed(nmea=nmea)

    def _update_boat_lat(self, nmea):
        """ Updates the boat's latitude.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'latitude'

        Side Effects:
        Sends boat data to the airmar broadcaster.
        """
        if nmea.latitude is not None:
            boat_lat = float(nmea.latitude)
            self.broadcaster.read_boat_latitude(boat_lat=boat_lat)

    def _update_boat_long(self, nmea):
        """ Updates the boat's longitude.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'longitude'

        Side Effects:
        Sends boat data to the airmar broadcaster
        """
        if nmea.longitude is not None:
            boat_long = float(nmea.longitude)
            self.broadcaster.read_boat_longitude(boat_long=boat_long)

    def _update_boat_head(self, nmea):
        """ Updates the boat's true_track.
        Keyword arguments:
        nmea -- a NMEASentence object containing 'true_track'

        Side Effects:
        Sends boat data to the airmar broadcaster
        """
        if nmea.true_track is not None:
            boat_head = float(nmea.true_track) % 360
            self.broadcaster.read_boat_heading(boat_head=boat_head)

    def _update_boat_speed(self, nmea):
        """ Updates the boat's speed.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'spd_over_grnd_kmph'

        Side Effects:
        Sends boat data to the airmar broadcaster
        """
        if nmea.spd_over_grnd_kmph is not None:
            boat_speed = float(nmea.spd_over_grnd_kmph)
            self.broadcaster.read_boat_speed(boat_speed=boat_speed)
