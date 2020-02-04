from threading import Thread

from pubsub import pub

class LiDARReader(Thread):
    """Class that receives information from LiDAR sensor"""
    def __init__(self, boat):
        """Initializes LiDAR reader class"""
        super().__init__()

        self.boat = boat

    def run(self):
        """
        Starts LiDAR reading
        """
        while self.keep_reading:
            # get sensor angle from boat
            sensor_ang = self.boat.current_sensor_ang()

            # send data over pub
            pub.sendMessage("LiDAR data", rng = self.rng, bearing=sensor_ang)
        else:
            pass

    def stop(self):
        """Pauses current thread without killing it"""
        self.keep_reading = False

