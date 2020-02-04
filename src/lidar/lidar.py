from threading import Thread, Lock
from time import sleep
from pubsub import pub
from math import floor

mutex = Lock()

class LiDAR(Thread):
    """Class that receives information from LiDAR sensor"""
    def __init__(self, boat):
        """Initializes LiDAR reader class"""
        super().__init__()

        self.boat = boat

        self.publish_interval = 0.5
        self.keep_reading = True
        self.quit_thread = False

        # subscribe to LiDAR pubsub channel
        pub.subscribe(self.store_rng, 'LiDAR raw data')

        # initialize raw data array
        self.raw_data = [0] * 5

    def run(self):
        """Publishes data from LiDAR"""
        while self.keep_reading:
            if self.quit_thread:
                break
            self.publish()
            sleep(self.publish_interval)

    def store_rng(self, rng):
        """
        Stores raw range data in raw data array
        Inputs:
            rng -- raw range data from LiDAR
        Side Effects:
            self.raw_data -- pushes back raw data
        """
        mutex.acquire()
        self.raw_data[1:len(self.raw_data)] = self.raw_data[0:len(self.raw_data) - 1]
        self.raw_data[0] = rng
        mutex.release()

    def publish(self):
        """
        Publishes range data (if verified)
        """
        # CRITERIA -- need 3 of 5 range values to be within 0.1m of median val
        mutex.acquire()
        sorted_data = sorted(self.raw_data)
        mutex.release()
        med_idx = floor(len(sorted_data) / 2.)
        med = sorted_data[med_idx]
        if (abs(med - sorted_data[med_idx - 1]) <= 0.1) and (abs(med - sorted_data[med_idx + 1]) <= 0.1):
            # make sure that median is not <bad data value> (-1)
            if med != -1:
                pub.sendMessage("LiDAR data", rng=med, bearing=self.boat.get_current_sensor_value())

    def exit(self):
        """Quits run thread"""
        self.keep_reading = False
