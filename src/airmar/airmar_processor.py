import math

class AirmarProcessor:
    """Defines an airmar data processor that stores airmar data given a NMEASentence object"""

    def __init__(self):
        """Initializes a new airmar data processor.

        Returns:
        A new AirmarProcessor
        """
        self.airmar_data = {
            "WIND_SPEED_CURRENT": None,
            "WIND_SPEED_AVERAGE": None,
            # wind heading in degrees
            "WIND_HEADING_CURRENT": None,
            "WIND_HEADING_AVERAGE": None,
            "BOAT_LATITUDE": None,
            "BOAT_LONGITUDE": None,
            "BOAT_HEADING": None,
            "BOAT_SPEED": None
        }

    def update_airmar_data(self, nmea):
        """ Updates the wind and boat data in the ship data dictionary given a NMEASentence object

        Keyword arguments:
        nmea -- a NMEASentence object containing wind and boat data.
        """
        self._update_wind_data(nmea=nmea)
        self._update_boat_data(nmea=nmea)

    def get_airmar_data(self):
        """ Retrieves the current airmar_data dictionary from the processor

        Returns:
        A dictionary with keys:
            'WIND_SPEED_CURRENT', 'WIND_SPEED_AVERAGE',
            'WIND_HEADING_CURRENT', 'WIND_HEADING_AVERAGE',
            'BOAT_LATITUDE', 'BOAT_LONGITUDE', 'BOAT_HEADING', and
            'BOAT_SPEED' associated to floats representing current values of resepective keys.
        """
        return self.airmar_data


    ### --- WIND UPDATES --- ###

    def _update_wind_data(self, nmea):
        """ Updates the current and average wind speed and heading if availible.

        Keyword arguments:
        nmea -- a NMEASentence object containing wind_speed_meters
            and direction_true

        Side Effects:
        Updates processor's dictionary 'airmar_data'
        """
        if nmea.wind_speed_meters is not None and nmea.direction_true is not None:
            wind_speed = float(nmea.wind_speed_meters)
            wind_head = float(nmea.wind_direction_true)
            self.airmar_data["WIND_SPEED_CURRENT"] = wind_speed
            self.airmar_data["WIND_HEADING_CURRENT"] = wind_head

            self._update_wind_averages(wind_speed=wind_speed, wind_angle=wind_head)

    def _update_wind_averages(self, wind_speed, wind_angle):
        """ Calculates and writes to the ship data the average wind speed and heading.

        Keyword arguments:
        airmar_data -- the 'old' wind speed and direction averages
        wind_speed -- the current wind speed read in meters.
        wind_direc -- the current wind heading read in degrees.

        Side Effects:
        Updates processor's dictionary 'airmar_data'
        """
        wind_angle = math.radians(wind_angle)
        wind_angle_old = math.radians(self.airmar_data["WIND_HEADING_AVERAGE"])

        wind_speed_old = self.airmar_data["WIND_SPEED_AVERAGE"]

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

        self.airmar_data["WIND_SPEED_AVERAGE"] = speed
        self.airmar_data["WIND_HEADING_AVERAGE"] = heading


    ### --- BOAT UPDATES ---- ###

    def _update_boat_data(self, nmea):
        """ Updates the boat's latitude, longitude, heading and speed

        Keyword arguments:
        nmea -- a NMEASentence object containing 'latitude', 'longitude', 'heading', and 'speed'

        Side Effects:
        Updates processor's dictionary 'airmar_data'
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
        Updates processor's dictionary 'airmar_data'
        """
        if nmea.latitude is not None and float(nmea.latitude) > 10:
            self.airmar_data["BOAT_LATITUDE"] = float(nmea.latitude)

    def _update_boat_long(self, nmea):
        """ Updates the boat's longitude. Only accepts values < -10

        Keyword arguments:
        nmea -- a NMEASentence object containing 'longitude'

        Side Effects:
        Updates processor's dictionary 'airmar_data'
        """
        if nmea.longitude is not None and float(nmea.longitude) < -10:
            self.airmar_data["BOAT_LONGITUDE"] = float(nmea.longitude)

    def _update_boat_head(self, nmea):
        """ Updates the boat's heading.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'heading'

        Side Effects:
        Updates processor's dictionary 'airmar_data'
        """
        if nmea.heading is not None:
            self.airmar_data["BOAT_HEADING"] = float(nmea.heading) % 360

    def _update_boat_speed(self, nmea):
        """ Updates the boat's speed.

        Keyword arguments:
        nmea -- a NMEASentence object containing 'speed'

        Side Effects:
        Updates processor's dictionary 'airmar_data'
        """
        if nmea.speed is not None:
            self.airmar_data["BOAT_SPEED"] = float(nmea.speed)
