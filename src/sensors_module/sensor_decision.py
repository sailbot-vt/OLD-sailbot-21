from threading import Thread

from src.sensor_movement.config_reader import read_decision_config

class SensorDecision(Thread):
    """Class that contains decision making logic for sensor module"""
    def __init__(self):
        """Initializes SensorDecision class"""
        super().__init__()

        config = read_decision_config()        
