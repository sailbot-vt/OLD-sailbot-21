"""
Expected messgae to be object such that:
    RCComand
        TURN_RUDDER = n
        TRIM_SAIL = n
    -Both values are realtive and signed.
    -For TRIM_SAIL positive brings the winch in.
"""
from threading import Thread
from src.msg import msg
from enum import Enum
from src.rudder.rudder_servo_controller import RudderServoController
import Adafruit_BBIO

""" I don't know where to put these constants
Most need to be determined by testing"""
pwm_pin = 1 #Need to figure out
duty_max = 0
duty_min = 0
angle_max = 180
angle_min = -180
mechanical_advantage = 1

rudder_control = None

class RudderThread(Thread):
    """ Thread to subscribe and move the servo as such."""

    def run(self):
        """
        Entry point.
        Not sure if this will run multiple times
        """
        pwm_pin = Adafruit_BBIO.PWM
        global rudder_control
        rudder_control = RudderServoController(pwm_pin, duty_min, duty_max, angle_min, angle_max, mechanical_advantage)
        rc_command_subscriber = msg.Subscribe("RCComand", "rc_command_callback_function")

    def rc_command_callback_function(data):
        if not data.TURN_RUDDER is None:
            delta_rudder_angle = data.TURN_RUDDER
            rudder_control.change_rudder_angle(delta_rudder_angle)


class TestableRudderSubscriber():
    """
    Mock subscriber to feed artifical input to the rudder_control
    """
    def __init__(self):
        """
        Make a bunch of angles to turn.
        """
        self.delta_angles = [0, -0, 15, -15, 90, -90, 90, 90, -180, 90]

    def rc_command_callback_function(self):
        """
        Mock this method as it is the one that is called.
        """
        for angle in self.delta_angles:
            self.rudder_control.change_rudder_angle(angle)

class RudderSubscriberType(Enum):
    Testable = 0,
    Production = 1


def make_rudder_subscriber(rudder_subscriber_type, channelName="RCComand", functionName = "rc_command_callback_function"):
    """
    Create a subscriber that is real or mocked for the purpose of testing.

    Keyword arguments:
    rudder_subscriber_type -- The type of subscriber to create

    Returns:
    The correct type of subscriber.
    """
    if rudder_subscriber_type == RudderSubscriberType.Testable:
        return TestableRudderSubscriber()

    return msg.Subscribe(channelName, functionName)
