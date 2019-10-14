import json

from pubsub import pub


class AirmarSocket:
    """ Process airmar data from pubsub """
    @property
    def serialized_data(self):
        """ Gets the latest airmar data in a serialized format 
        
        Returns:
        Json dump (serialized) of the airmar data
        """
        return json.dumps({
                "true_wind_speed": self.true_wind_speed,
                "true_wind_angle": self.true_wind_angle,
                "apparent_wind_speed": self.apparent_wind_speed,
                "apparent_wind_angle": self.apparent_wind_angle,
                "boat_latitude": self.boat_latitude,
                "boat_longitude": self.boat_longitude,
                "boat_heading": self.boat_heading,
                "boat_speed": self.boat_speed
            })

    def __init__(self):
        self.true_wind_speed = 0
        self.true_wind_angle = 0
        self.apparent_wind_speed = 0
        self.apparent_wind_angle = 0
        
        self.boat_latitude = 0
        self.boat_longitude = 0
        self.boat_heading = 0
        self.boat_speed = 0

        pub.subscribe(self.update_true_wind_angle, "wind angle true")
        pub.subscribe(self.update_true_wind_speed, "wind speed true")
        pub.subscribe(self.update_apparent_wind_angle, "wind angle apparent")
        pub.subscribe(self.update_apparent_wind_speed, "wind speed apparent")
        pub.subscribe(self.update_boat_latitude, "boat latitude")
        pub.subscribe(self.update_boat_longitude, "boat longitude")
        pub.subscribe(self.update_boat_speed, "boat speed")
        pub.subscribe(self.update_boat_heading, "boat heading")
    
    def update_true_wind_angle(self, angle):
        """ Updates the true wind angle"""
        self.true_wind_angle = angle

    def update_true_wind_speed(self, speed):
        """ Updates the true wind speed"""
        self.true_wind_speed = speed

    def update_apparent_wind_angle(self, angle):
        """ Updates the apparent wind angle"""
        self.apparent_wind_angle = angle

    def update_apparent_wind_speed(self, speed):
        """ Updates the apparent wind speed"""
        self.apparent_wind_speed = speed

    def update_boat_latitude(self, latitude):
        """ Updates the boat latitude"""
        self.boat_latitude = latitude

    def update_boat_longitude(self, longitude):
        """ Updates the boat longitude"""
        self.boat_longitude = longitude

    def update_boat_heading(self, angle):
        """ Updates the boat heading"""
        self.boat_heading = angle

    def update_boat_speed(self, speed):
        """ Updates the boat speed"""
        self.boat_speed = speed