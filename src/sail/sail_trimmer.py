"""
Expected messgae to be object such that:
    RCComand
        TURN_RUDDER = n
        TRIM_SAIL = n
    -Both values are realtive and signed.
    -For TRIM_SAIL positive brings the winch in.
"""
from threading import Thread
import SailServoController

""" I don't know where to put these constants
Most need to be determined by testing"""
pwm_pin = 1 #Need to figure out
duty_max = 0
duty_min = 0
angle_max = 180
angle_min = -180
mechanical_advantage = 1


class sailThread(Thread):
    """ Thead to subscribe and move the servo as such."""
    def __init__(self):
        """
        Create the thead
        """
        Thread.__init__(self)

    def run(self):
        """
        Entry point.
        Not sure if this will run multiple times
        """
        sail_control = sail_servo_controller(pwm_pin,duty_min,duty_max,angle_min,angle_max)
        subscriber = sail_consumer()


class sail_consumer(consumer):
    def register_to_consume_data(self, channel_name):
        pass
    def data_callback(self, data):
        delta_sail_angle = data.TRIM_SAIL
        sail_control.change_sail_angle(delta_sail_angle)
