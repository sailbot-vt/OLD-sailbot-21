"""
Expected messgae to be object such that:
    RCComand
        TURN_RUDDER = n
        TRIM_SAIL = n
    -Both values are realtive and signed.
    -For TRIM_SAIL positive brings the winch in.
"""
from threading import Thread
from enum import Enum

from pubsub import pub

from src.sail.sail_servo_controller import SailServoController

""" I don't know where to put these constants
Most need to be determined by testing"""
pwm_pin = 1 #Need to figure out
duty_max = 0
duty_min = 0
angle_max = 180
angle_min = -180
mechanical_advantage = 1

sail_control = None

class SailThread(Thread):
    """ Thead to subscribe and move the servo as such."""

    def run(self):
        """
        Entry point.
        Not sure if this will run multiple times
        """
        global sail_control
        sail_control = SailServoController(pwm_pin, duty_min, duty_max, angle_min, angle_max)
        rc_command_subscriber = pub.subscribe("RCComand", self.rc_command_callback_function)

    def rc_command_callback_function(self, data):
        if not data.TRIM_SAIL is None:
            delta_sail_angle = data.TRIM_SAIL
            sail_control.change_sail_angle(delta_sail_angle)

class TestableSailSubscriber():
    """
    Mock subscriber to feed artifical input to the rudder_control
    """
    def __init__(self):
        """
        Make a bunch of angles to turn.
        """
        self.delta_angles = [0, 1, 15, -16, 90, -90, 45, 45, -90]

    def rc_command_callback_function(self):
        """
        Mock this method as it is the one that is called.
        """
        for angle in self.delta_angles:
            self.sail_control.change_sail_angle(angle)

class SailSubscriberType(Enum):
    Testable = 0,
    Production = 1


def make_sail_subscriber(sail_subscriber_type, channelName="RCComand", functionName = "rc_command_callback_function"):
    """
    Create a subscriber that is real or mocked for the purpose of testing.

    Keyword arguments:
    rudder_subscriber_type -- The type of subscriber to create

    Returns:
    The correct type of subscriber.
    """
    if sail_subscriber_type == SailSubscriberType.Testable:
        return TestableSailSubscriber()

    return pub.subscribe(channelName, functionName)
