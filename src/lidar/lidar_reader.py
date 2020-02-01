from threading import Thread

from pubsub import pub

from src.lidar.config_reader import read_pin_config, read_interval, read_port_config

class LiDARReader(Thread):
    """Class that receives information from LiDAR sensor"""
    def __init__(self, boat, mock_bbio, mock_port):
        """Initializes LiDAR reader class"""
        super().__init__()

        # set up pin and port for serial comms
        pin = read_pin_config(mock_bbio=mock_bbio)
        port = read_port_config(mock_port=mock_port)

        self.keep_reading = True
        self.read_interval = read_interval()

        self.boat = boat

    def run(self):
        """
        Starts LiDAR reading
        """
        while self.keep_reading:
            # read sentence from port
            self.read_sentence()

            # get sensor angle from boat
            sensor_ang = self.boat.current_sensor_ang()

            # send data over pub
            pub.sendMessage("LiDAR data", rng = self.rng, bearing=sensor_ang)
        else:
            pass

    def stop(self):
        """Pauses current thread without killing it"""
        self.keep_reading = False

    # TODO SET UP RECEIVER
