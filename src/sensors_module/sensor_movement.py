from pubsub import pub

from src.sensor_movement.config_reader import read_config 

class SensorMovement:
    """Thread to maintain sensor module system state and drive movement."""
    def __init__(self, boat, world):
        super().__init__()
        pub.subscribe(self.move_sensor, "set sensor to")

    def move_sensor(self, bearing):
        """
        Sends command to arduino module to move sensor
        Inputs:
            bearing -- bearing to move to (in deg)
        """
        pub.sendMessage('turn sensor to', sensor_ang=bearing)
