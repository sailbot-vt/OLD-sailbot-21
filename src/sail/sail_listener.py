from pubsub import pub

from src.sail.config_reader import read_pin_config, read_mainsheet_config 
from src.sail.mainsheet import Mainsheet

class SailListener:
    """Thread to maintain sail system state and auto-drive as necessary."""
    def __init__(self, boat, world):
        super().__init__()
        mainsheet_config = read_mainsheet_config()
        self.mainsheet = Mainsheet(mainsheet_config)
        pub.subscribe(self.trim_boom_to, "set trim")
        pub.subscribe(self.trim_in_by, "set trim in")
