import math

from threading import Lock

from src.airmar.airmar_exceptions import InvalidIDException, UnsupportedIDException
from src.utils.vec import Vec2


class AirmarProcessor:
    """ Processes raw data from airmar and publishes to the specified
    broadcaster """

    def __init__(self, broadcaster, parser):
        """ Builds an airmar processor to process raw airmar data.

        Keyword Arguments:
        broadcaster -- data broadcast type
        parser -- nmea parser to map raw data.

        Returns:
        A new airmar processor
        """
        self.parser = parser
        self.broadcaster = broadcaster

        self.data = {}

    def update_airmar_data(self, nmea):
        """ Updates airmar data from given nmea fields. 
        
        Keyword Arguments:
        nmea -- A list of fields parsed from an nmea sentence

        Side effects:
        Broadcasts updated processed data.

        Raises:
        InvalidIDException for invalid sentence ids.
        UnsupportedIDException when program does not implement
        interface to parse given nmea fields.
        """
        raw = {}
        sid = nmea[0]

        self.parser.update_data(data=raw, fields=nmea)
        
        if sid == "WIVWR":
            self._update_wind(raw=raw, sid=sid, 
                speed_key="wind speed apparent",
                angle_key="wind angle apparent")
        elif sid == "WIVWT":
            self._update_wind(raw=raw, sid=sid, 
                speed_key="wind speed true",
                angle_key="wind angle true")
        elif sid == "GPGGA":
            self._update_boat_gps(raw=raw, sid=sid)
        elif sid == "GPVTG":
            self._update_boat_speed(raw=raw, sid=sid)
        # Other updated processed data goes below

        # Broadcasts processed data via broadcaster
        self.broadcaster.publish_dictionary(data=self.data)



# --------------------  PROCESSED DATA ENTRY --------------------
    def _update_wind(self, raw, sid, speed_key, angle_key):
        """ Updates scaled average wind speed and heading direction. 
        
        Keyword Arguments:
        raw -- The dictionary containing the raw WIVWR or WIVWT data.
            representing relative or true wind data respectively.
        sid -- nmea sentence id representing true or relative wind data.
        speed_key -- The key in broadcaster containing the speed data in mps
        angle_key -- The key in broadcaster containing the angle data in degrees
        """
        # Left is negative, Right is positive
        if (raw[sid]["wind_angle_direction"]) == "L":
            # (counter clockwise)
            # i.e -1 degree = 359 degree.
            raw[sid]["wind_angle_degree"] = (360 - float(raw[sid]["wind_angle_degree"])) % 360
        
        # Initialize new speed to data
        if speed_key not in self.data:
            self.data[speed_key] = float(raw[sid]["wind_speed_mps"])
        if angle_key not in self.data:
            self.data[angle_key] = float(raw[sid]["wind_angle_degree"])

        # Calculated weighted magn and angle from old and new data.
        self.data[speed_key], self.data[angle_key] = self._scale_avg_polar_coords(
            o_magn=self.data[speed_key],
            o_angle=self.data[angle_key],
            n_magn=float(raw[sid]["wind_speed_mps"]),
            n_angle=float(raw[sid]["wind_angle_degree"])
        )

    def _update_boat_gps(self, raw, sid):
        """ Updates the boat's latitude and longitude position in minutes.
        
        Keyword Arguments:
        raw -- The dictionary containing raw gps data.
        sid -- gps nmea sentence id.
        """
        self.data["boat latitude"] = float(raw[sid]["latitude"])
        self.data["boat longitude"] = float(raw[sid]["longitude"])

    def _update_boat_speed(self, raw, sid):
        """ Updates the boat's speed and heading direction in kph and minutes.

        Keyword Arguments:
        raw -- The dictionary containig the raw speed and course data
        sid -- speed/heading nmea sentence id.
        """
        self.data["boat speed"] = float(raw[sid]["speed_over_ground_kph"])
        self.data["boat heading"] = float(raw[sid]["course_over_ground_true"])



# -------------------- AIRMAR SPECIFIC CALCULATIONS --------------------
    def _scale_avg_polar_coords(self, o_magn, o_angle, n_magn, n_angle):
        """ Calculates the scaled average polar coordinates given the original
        polar coordinates and new polar coordinates. Note, the scaled weight
        will be 70% of the original + 30% new vectors.

        Keyword Arguments:
        o_magn -- The magnitude of the original vector.
        o_angle -- The angle of the original vector in degrees.
        n_magn -- The magnitude of the new vector.
        n_angle -- the angle of the new vector in degrees.

        Returns:
        (magnitude, angle) as a tuple, such that the magnitude and angle in 
        degrees of the vector is the scaled average of the original and new vector.
        """
        old = Vec2.build_from(magnitude=o_magn, angle=math.radians(o_angle))
        new = Vec2.build_from(magnitude=n_magn, angle=math.radians(n_angle))
        
        # Weighted average
        weight = 0.3
        x = (old.x * (1 - weight)) + (new.x * weight)
        y = (old.y * (1 - weight)) + (new.y * weight)
        
        v = Vec2(x, y)

        # Convert to degrees, returns tuple (speed, angle)
        try:
            v_angle = math.degrees(v.angle())
        except ZeroDivisionError:
            v_angle = 0

        # Assume counter clockwise. More details in documentation.
        degrees = v_angle if v_angle >=0 else 360 + v_angle
        return v.length(), degrees
