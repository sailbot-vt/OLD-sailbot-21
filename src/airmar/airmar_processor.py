import math

class AirmarProcessor:
    """Defines an airmar data processor that stores ship data given a pnmea2 object"""

    def __init__(self):
        """Initializes a new airmar data processor.

        Returns:
        A new AirmarProcessor
        """
        self.ship_data = {
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

    def update_data(self, data):
        """ Updates the wind and boat data in the ship data dictionary given a pnmea2 object

        Keyword arguments:
        data -- a pynmea2 object containing wind and boat data.
        """
        self._update_wind_data(data=data)
        self._update_boat_data(data=data)

    def get_data(self):
        """ Retrieves the current ship_data dictionary from the processor

        Returns:
        A dictionary with keys:
            'WIND_SPEED_CURRENT', 'WIND_SPEED_AVERAGE',
            'WIND_HEADING_CURRENT', 'WIND_HEADING_AVERAGE',
            'BOAT_LATITUDE', 'BOAT_LONGITUDE', 'BOAT_HEADING', and
            'BOAT_SPEED' associated to floats representing current values of resepective keys.
        """
        return self.ship_data


    ### --- WIND UPDATES --- ###

    def _update_wind_data(self, data):
        """ Updates the current and average wind speed and heading if availible.

        Keyword arguments:
        data -- a pynmea2 object containing wind_speed_meters
            and direction_true

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        if data.wind_speed_meters is not None and data.direction_true is not None:
            wind_speed = float(data.wind_speed_meters)
            wind_head = float(data.wind_direction_true)
            self.ship_data["WIND_SPEED_CURRENT"] = wind_speed
            self.ship_data["WIND_HEADING_CURRENT"] = wind_head

            self._update_wind_averages(wind_speed=wind_speed, wind_angle=wind_head)

    def _update_wind_averages(self, wind_speed, wind_angle):
        """ Calculates and writes to the ship data the average wind speed and heading.

        Keyword arguments:
        ship_data -- the 'old' wind speed and direction averages
        wind_speed -- the current wind speed read in meters.
        wind_direc -- the current wind heading read in degrees.

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        wind_angle = math.radians(wind_angle)
        wind_angle_old = math.radians(self.ship_data["WIND_HEADING_AVERAGE"])

        wind_speed_old = self.ship_data["WIND_SPEED_AVERAGE"]

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

        self.ship_data["WIND_SPEED_AVERAGE"] = speed
        self.ship_data["WIND_HEADING_AVERAGE"] = heading


    ### --- BOAT UPDATES ---- ###

    def _update_boat_data(self, data):
        """ Updates the boat's latitude, longitude, heading and speed

        Keyword arguments:
        data -- a pynmea2 object containing 'latitude', 'longitude', 'heading', and 'speed'

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        self._update_boat_lat(data=data)
        self._update_boat_long(data=data)
        self._update_boat_head(data=data)
        self._update_boat_speed(data=data)

    def _update_boat_lat(self, data):
        """ Updates the boat's latitude. Only accepts values > 10.

        Keyword arguments:
        data -- a pynmea2 object containing 'latitude'

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        if data.latitude is not None and float(data.latitude) > 10:
            self.ship_data["BOAT_LATITUDE"] = float(data.latitude)

    def _update_boat_long(self, data):
        """ Updates the boat's longitude. Only accepts values < -10

        Keyword arguments:
        data -- a pynmea2 object containing 'longitude'

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        if data.longitude is not None and float(data.longitude) < -10:
            self.ship_data["BOAT_LONGITUDE"] = float(data.longitude)

    def _update_boat_head(self, data):
        """ Updates the boat's heading.

        Keyword arguments:
        data -- a pynmea2 object containing 'heading'

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        if data.heading is not None:
            self.ship_data["BOAT_HEADING"] = float(data.heading) % 360

    def _update_boat_speed(self, data):
        """ Updates the boat's speed.

        Keyword arguments:
        data -- a pynmea2 object containing 'speed'

        Side Effects:
        Updates processor's dictionary 'ship_data'
        """
        if data.speed is not None:
            self.ship_data["BOAT_SPEED"] = float(data.speed)
