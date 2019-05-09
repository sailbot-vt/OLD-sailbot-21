from threading import Thread

from pubsub import pub

from src.hardware.servo import Servo
from src.sail.config_reader import build_pin_from_config, read_servo_config, \
    read_mainsheet_config
from src.sail.mainsheet import Mainsheet


class SailThread(Thread):
    """Thread to maintain sail system state and auto-drive as necessary."""
    def __init__(self):
        super().__init__()
        servo = Servo(build_pin_from_config(), read_servo_config())
        self.mainsheet = Mainsheet(servo, read_mainsheet_config())
        pub.subscribe(self.received_trim_command, "set trim")

    def received_trim_command(self, degrees_in):
        self.mainsheet.trim_in_by(degrees_in)
