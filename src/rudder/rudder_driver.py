"""
Expected messgae to be object such that:
    RCComand
        TURN_RUDDER = n
        TRIM_SAIL = n
    -Both values are realtive and signed.
    -For TRIM_SAIL positive brings the winch in.
"""
from threading import Thread
from src.msg_system.consumer import consumer
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

class RudderThread(Thread):
    """ Thread to subscribe and move the servo as such."""

    def run(self):
        """
        Entry point.
        Not sure if this will run multiple times
        """
        pwm_pin = Adafruit_BBIO.PWM
        rudder_control = RudderServoController(pwm_pin, duty_min, duty_max, angle_min, angle_max, mechanical_advantage, pwm_lib)
        subscriber = make_rudder_consumer(RudderConsumerType.Production)
        subscriber.register_to_consume_data("RCComand")


class RudderConsumer(consumer):
    """
    Acts as a subscriber for the rudder. Extends consumer.
    """
    def register_to_consume_data(self, channel_name):
        pass
    def data_callback(self, data):
        """
        Function that is called when data is sent on the channel.
        """
        if not data.TURN_RUDDER is None:
            delta_rudder_angle = data.TURN_RUDDER
            self.rudder_control.change_rudder_angle(delta_rudder_angle)

class TestableRudderConsumer():
    """
    Mock consumer to feed artifical input to the rudder_control
    """
    def __init__(self):
        """
        Make a bunch of angles to turn.
        """
        self.delta_angles = [0, -0, 15, -15, 90, -90, 90, 90, -180, 90]

    def register_to_consume_data(self, data):
        """
        Mock this method as it is the one that is called.
        """
        for angle in self.delta_angles:
            self.rudder_control.change_rudder_angle(angle)

class RudderConsumerType(Enum):
    Testable = 0,
    Production = 1


def make_rudder_consumer(rudder_consumer_type):
    """
    Create a consumer that is real or mocked for the purpose of testing.

    Keyword arguments:
    rudder_consumer_type -- The type of consumer to create

    Returns:
    The correct type of consumer.
    """
    if rudder_consumer_type == RudderConsumerType.Testable:
        return TestableRudderConsumer()

    return RudderConsumer()
