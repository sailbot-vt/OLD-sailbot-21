import math

class AirmarProcessor:
    """ TODO temprorary processor to be refactored into separate data objects
    to handle more nmea sentences """
    def __init__(self, broadcaster):
        self.broadcaster = broadcaster
        self.data = {
            "wind speed" : None,
            "wind heading" : None,
            "boat latitude": None,
            "boat longitude": None,
            "boat heading" : None,
            "boat speed": None
        }

    def update_airmar_data(self, nmea):
        # GPVTG, GPGGA, WIMWD, WIVWR
        # Field numeration taken from airmar manual
        sid = nmea[0]
        if sid is None:
            # Sentence identifier not given.
            return
        elif sid is "GPVTG":
            # <1> Course over ground degrees True, to nearest 0.1 degree
            # <7> Speed over ground, km/h to the nearest 0.1 km/h
            if nmea[7] is None or nmea[1] is None:
                return
            self._update_boat_speed(nmea[7], nmea[1])
        elif sid is "GPGGA":
            # <2> Latitude <4> Longitude: to nearest .0001 minutes
            if nmea[2] is None or nmea[4] is None:
                return
            self._update_boat_gps(nmea[2], nmea[4])
        elif sid is "WIMWD":
            # <1> Wind direction, 0.0 to 359.9 degrees True to nearest .1 degree
            # <7> Wind speed, meters/second, to nearest 0.1 m/s
            if nmea[7] is None or nmea[1] is None:
                return
            self._update_wind(nmea[7], nmea[1])
        elif sid is "WIVWR":
            # <1> Measured wind angle relative to vessel, 0 to 180 degrees,
            #   left/right of vessel heading, to the nearest 0.1 degree
            # <2> L = left, or R = right
            # <3> Measured wind speed, knots to the nearest 0.1 knot
            # <5> Wind speed, meters per second to the nearest 0.1 m/s
            # <7> Wind speed, km/h to the nearest km/h
            # TODO Implement this to data dictionary
            return
        else:
            # Sentence not known.
            return
        self.broadcaster.update_data(data=self.data)

        # TODO should I broadcast data from processor?
        # or control manually
        for key in self.data.keys():
            self.broadcaster.read_data(key=key)

    def _update_wind(self, wind_speed, wind_angle):
        # This was taken from old code for averages.
        if self.data["wind heading"] is None:
            self.data["wind heading"] = wind_angle
        if self.data["wind speed"] is None:
            self.data["wind speed"] = wind_speed
        
        wind_angle = math.radians(wind_angle)
        wind_angle_old = math.radians(self.data["wind heading"])

        wind_speed_old = self.data["wind speed"]

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
        self.data["wind speed"] = speed
        self.data["wind heading"] = heading
        

    def _update_boat_gps(self, latitude, longitude):
        self.data["boat latitude"] = float(latitude)
        self.data["boat longitude"] = float(longitude)

    def _update_boat_speed(self, speed, head):
        self.data["boat speed"] = float(speed)
        self.data["boat heading"] = float(head) % 360
    