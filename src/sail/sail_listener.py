from pubsub import pub

from src.sail.config_reader import read_pin_config, read_center_stepper_angle
from src.sail.stepper import StepperTrimmer


class SailListener:
    """Thread to maintain sail system state and auto-drive as necessary."""
    def __init__(self, boat, world):
        super().__init__()
        self.stepper = StepperTrimmer(read_pin_config(), read_center_stepper_angle(), boat, world)
        pub.subscribe(self.received_trim_command, "set trim")

    def received_trim_command(self, degrees_in):
        self.stepper.trim_in_by(degrees_in)
