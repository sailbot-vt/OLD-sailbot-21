import math

from threading import Lock


class AirmarProcessor:
    def __init__(self, broadcaster, parser):
        self.parser = parser
        self.broadcaster = broadcaster
        self.data = {
            "wind speed apparent" : None,
            "wind angle apparent" : None,
            "wind speed true": None,
            "wind angle true": None,
            "boat latitude": None,
            "boat longitude": None,
            "boat heading" : None,
            "boat speed": None
        }
        self.raw = {}

    def update_airmar_data(self, nmea):
        sid = nmea[0]
        if sid is None:
            return
        self.parser.update_data(data=self.raw, fields=nmea)

        # TODO Update list with more interfaces
        if sid in ["WIVWT", "WIVWR"]:
            self._update_wind(sid)
        elif sid in ["GPGGA"]:
            self._update_boat_gps(sid)
        elif sid in ["GPVTG"]:
            self._update_boat_speed(sid)
        
        # Broadcasts processed data via broadcaster
        self.broadcaster.update_dictionary(data=self.data)

    def _update_wind(self, sid):
        speed_key = "wind speed apparent"
        angle_key = "wind angle apparent"
        if sid is "WIVWT":
            # Update true wind values instead
            speed_key = "wind speed true"
            angle_key = "wind angle true"
        # Set old values = new values if no old values
        if self.data[angle_key] is None:
            self.data[angle_key] = float(self.raw[sid]["wind_angle_degree"]) % 360
        if self.data[speed_key] is None:
            self.data[speed_key] = float(self.raw[sid]["wind_speed_mps"])

        self.data[speed_key], self.data[angle_key] = self._scale_avg_polar_coords(
            old_magnitude=self.data[speed_key],
            old_angle=self.data[angle_key],
            new_magnitude=float(self.raw[sid]["wind_speed_mps"]),
            new_angle=float(self.raw[sid]["wind_angle_degree"]) % 360
        )

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

        return math.sqrt(x*x + y*y), math.degrees(math.atan2(x, y)) % 360

    def _update_boat_gps(self, sid):
        if sid in self.raw:
            self.data["boat latitude"] = float(self.raw[sid]["latitude"])
            self.data["boat longitude"] = float(self.raw[sid]["longitude"])

    def _update_boat_speed(self, sid):
        if sid in self.raw:
            self.data["boat speed"] = float(self.raw[sid]["speed_over_ground_kph"])
            self.data["boat heading"] = float(self.raw[sid]["course_over_ground_true"]) % 360
    