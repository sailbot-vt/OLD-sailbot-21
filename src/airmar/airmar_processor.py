import math

from threading import Lock


class AirmarProcessor:
    def __init__(self, broadcaster, parser):
        self.parser = parser
        self.broadcaster = broadcaster

        self.data = {
            "wind speed apparent" : 0,
            "wind angle apparent" : 0,
            "wind speed true": 0,
            "wind angle true": 0,
            "boat latitude": 0,
            "boat longitude": 0,
            "boat heading" : 0,
            "boat speed": 0
        }
        self.raw = {}

    def update_airmar_data(self, nmea):
        sid = nmea[0]
        if sid is None:
            return
        self.parser.update_data(data=self.raw, fields=nmea)

        if sid == "WIVWR":
            self._update_wind(sid=sid, 
                speed_key="wind speed apparent",
                angle_key="wind angle apparent")
        if sid == "WIVWT":
            self._update_wind(sid=sid, 
                speed_key="wind speed true",
                angle_key="wind angle true")
        elif sid == "GPGGA":
            self._update_boat_gps(sid)
        elif sid == "GPVTG":
            self._update_boat_speed(sid)
        # Other updated processed data goes below

        # Broadcasts processed data via broadcaster
        self.broadcaster.update_dictionary(data=self.data)



# --------------------  PROCESSED DATA ENTRY --------------------
    def _update_wind(self, sid, speed_key, angle_key):
        # update speed and angle for given sid
        # Note, at start old values = 0, might skew values
        # TODO Test above if values are skewed.
        self.data[speed_key], self.data[angle_key] = self._scale_avg_polar_coords(
            old_magnitude=self.data[speed_key],
            old_angle=self.data[angle_key],
            new_magnitude=float(self.raw[sid]["wind_speed_mps"]),
            new_angle=float(self.raw[sid]["wind_angle_degree"]) % 360
        )

    def _update_boat_gps(self, sid):
        # Update boat latitude and longitude
        self.data["boat latitude"] = float(self.raw[sid]["latitude"])
        self.data["boat longitude"] = float(self.raw[sid]["longitude"])

    def _update_boat_speed(self, sid):
        # Update boat speed and heading
        self.data["boat speed"] = float(self.raw[sid]["speed_over_ground_kph"])
        self.data["boat heading"] = float(self.raw[sid]["course_over_ground_true"]) % 360


# -------------------- AIRMAR SPECIFIC CALCULATIONS --------------------
    def _scale_avg_polar_coords(self, old_magnitude, old_angle, new_magnitude, new_angle):
        # Convert to radians
        new_angle = math.radians(new_angle)
        old_angle = math.radians(old_angle)

        # Calculate components
        old_x = old_magnitude * math.sin(old_angle)
        old_y = old_magnitude * math.cos(old_angle)
        new_x = new_magnitude * math.sin(new_angle)
        new_y = new_magnitude * math.cos(new_angle)
        
        # Weighted values
        weight = 0.3
        x = old_x * (1 - weight) + new_x * weight
        y = old_y * (1 - weight) + new_y * weight

        # Convert to degrees, returns tuple (speed, angle)
        return math.sqrt(x*x + y*y), math.degrees(math.atan2(x, y)) % 360