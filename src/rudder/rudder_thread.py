from threading import Thread

from pubsub import pub

from src.hardware.servo import Servo
from src.rudder.config_reader import build_pin_from_config, read_servo_config, \
    read_rudder_config
from src.rudder.rudder import Rudder


class RudderThread(Thread):
    """Thread to maintain rudder system state and auto-drive as necessary."""
    def __init__(self):
        super().__init__()
        servo = Servo(build_pin_from_config(), read_servo_config())
        self.rudder_control = Rudder(servo, read_rudder_config())
        pub.subscribe(self.received_rudder_command, "set rudder")

    def received_rudder_command(self, degrees_starboard):
        self.rudder_control.change_rudder_angle(degrees_starboard)
