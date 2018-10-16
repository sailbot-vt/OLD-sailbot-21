from os import environ
from abc import ABC, abstractmethod


class RCReceiver(ABC):
    @abstractmethod
    def read_input(self):
        """Reads input from the RC receiver."""
        pass

    @abstractmethod
    def _scale_rudder_input(self, raw_value=0):
        """Scales the rudder values from the raw value to

        Keyword arguments:
        raw_value -- The raw rudder input.
        """
        pass

    @abstractmethod
    def _scale_trim_input(self, raw_value=0):
        """Scales the trim values from the raw value to

        Keyword arguments:
        raw_value -- The raw trim input.
        """
        pass


class TestableRCReceiver(RCReceiver):
    def read_input(self):
        pass

    def _scale_rudder_input(self, raw_value=0):
        pass

    def _scale_trim_input(self, raw_value=0):
        pass


class FSR6BRCReceiver(RCReceiver):
    def read_input(self):
        pass

    def _scale_rudder_input(self, raw_value=0):
        pass

    def _scale_trim_input(self, raw_value=0):
        pass


def make_rc_receiver():
    """Generates the appropriate implementation of RCReceiver.

    Implements the abstract factory pattern, except calls constructors instead of factory methods.

    Returns:
    The correct RCReceiver for the environment.
    """
    if environ["ENV"] == "test":
        return TestableRCReceiver()
    else:
        import Adafruit_BBIO.GPIO as GPIO
        return FSR6BRCReceiver()
