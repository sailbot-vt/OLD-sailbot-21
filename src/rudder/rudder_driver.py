"""
Expected messgae to be object such that:
    RCComand
        TURN_RUDDER = n
        TRIM_SAIL = n
    -Both values are realtive and signed.
    -For TRIM_SAIL positive brings the winch in.
"""
from threading import Thread
import RudderServoController


class rudderThread(Thread):
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
        rudder_control = rudder_servo_controller()"""TODO: add arguments"""
        subscriber = rudder_consumer()


class rudder_consumer(consumer):
    def register_to_consume_data(self, channel_name):
        pass
    def data_callback(self, data):
        delta_rudder_angle = data.TURN_RUDDER
        rudder_control.change_rudder_angle(delta_rudder_angle)
