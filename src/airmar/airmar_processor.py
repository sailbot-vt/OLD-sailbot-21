import math

class AirmarProcessor:
    def __init__(self):
        self.ship_data = {
            "WIND_SPEED_CURRENT": 0.0,
            "WIND_SPEED_AVERAGE": 0.0,
            # wind heading in degrees
            "WIND_DIRECTION_CURRENT": 0.0,
            "WIND_DIRECTION_AVERAGE": 0.0,
            "BOAT_LATITUDE": 0.0,
            "BOAT_LONGITUDE": 0.0,
            "BOAT_HEADING": 0.0,
            "BOAT_SPEED": 0.0
        }

    def update_data(self, data):
        self._update_wind_data(data=data)
        self._update_boat_data(data=data)
        pass


    ### --- WIND UPDATES --- ###

    def _update_wind_data(self, data):
        if data.wind_speed_meters is not None and data.direction_true is not None:
            wind_speed = float(data.wind_speed_meters)
            wind_direc = float(data.wind_direction_true)
            self.ship_data["WIND_SPEED_CURRENT"] = wind_speed
            self.ship_data["WIND_DIRECTION_CURRENT"] = wind_direc

            self._update_wind_averages(wind_speed=wind_speed, wind_direc=wind_direc)

    def _update_wind_averages(self, wind_speed, wind_direc):
        wind_direc = math.radians(wind_direc)
        wind_direc_old = math.radians(self.ship_data["WIND_DIRECTION_AVERAGE"])

        wind_speed_old = self.ship_data["WIND_SPEED_AVERAGE"]

        # calculate components
        old_x = wind_speed_old * math.cos(wind_direc_old)
        old_y = wind_speed_old * math.sin(wind_direc_old)

        new_x = wind_speed * math.cos(wind_direc)
        new_y = wind_speed * math.sin(wind_direc)

        # Weighted values
        weight = 0.3
        x = old_x * (1 - weight) + new_x * (weight)
        y = old_y * (1 - weight) + new_y * (weight)

        self.ship_data["WIND_SPEED_AVERAGE"] = math.sqrt(x*x + y*y)
        self.ship_data["WIND_DIRECTION_AVERAGE"] = math.degrees(math.atan2(x, y)) % 360


    ### --- BOAT UPDATES ---- ###

    def _update_boat_data(self, data):
        self._update_boat_lat(data=data)
        self._update_boat_long(data=data)
        self._update_boat_head(data=data)
        self._update_boat_speed(data=data)

    def _update_boat_lat(self, data):
        if data.latitude is not None and fload(data.latitude) > 10:
            self.ship_data["BOAT_LATITUDE"] = float(data.latitude)

    def _update_boat_long(self, data):
        if data.longitude is not None and float(data.longitude) < -10:
            self.ship_data["BOAT_LONGITUDE"] = float(data.longitude)

    def _update_boat_head(self, data):
        if data.heading is not None:
            self.ship_data["BOAT_HEADING"] = float(data.heading) % 360

    def _update_boat_speed(self, data):
        if data.speed is not None:
            self.ship_data["BOAT_SPEED"] = float(data.speed)
