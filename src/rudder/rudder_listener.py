from pubsub import pub

from src.rudder.config_reader import build_pin_from_config, \
    read_rudder_config
from src.rudder.rudder import Rudder


class RudderListener:
    """Thread to maintain rudder system state and auto-drive as necessary."""
    def __init__(self):
        self.rudder_control = Rudder(read_rudder_config())
        pub.subscribe(self.received_rudder_command, "set rudder")

    def received_rudder_command(self, degrees_starboard):
        self.rudder_control.change_rudder_angle(degrees_starboard)
