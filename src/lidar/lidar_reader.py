from threading import Thread
from time import sleep
from pubsub import pub

class LiDARReader(Thread):
    """Class that receives information from LiDAR sensor"""
    def __init__(self, boat):
        """Initializes LiDAR reader class"""
        super().__init__()

        self.boat = boat

        self.publish_interval = 0.5
        self.keep_reading = True

        # subscribe to LiDAR pubsub channel
        pub.subscribe(self.store_rng, 'LiDAR raw data')

        # initialize raw data array
        raw_data = [0] * 5

    def run(self):
        """Publishes data from LiDAR"""
        while self.keep_reading:
            self.publish()
            sleep(self.publish_interval)
        else:
            pass

    def store_rng(self, rng):
        """
        Stores raw range data in raw data array
        Inputs:
            rng -- raw range data from LiDAR
        Side Effects:
            self.raw_data -- pushes back raw data
        """
        raw_data[1:len(raw_data)] = raw_data[0:len(raw_data) - 1)
        raw_data[0] = rng

    def publish(self):
        """
        Publishes range data (if verified)
        """
        # TODO 
        pass

    def stop(self):
        """Stops run loop without killing it"""
        self.keep_reading = False

    def start(self):
        """Starts run loop (after being stopped)"""
        self.keep_reading = True
