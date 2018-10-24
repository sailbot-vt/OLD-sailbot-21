from os import environ
from threading import Timer
from abc import ABC
from src.rc_input.rc_broadcasting import make_broadcaster
from src.navigation_mode import NavigationMode


RC_READ_INTERVAL = 50


class RCReceiver(ABC):
    """Defines an RCReceiver type"""
    pass


class TestableRCReceiver(RCReceiver):
    """A mock RCReceiver to test consumers of RCReceiver."""
    def fake_read_input(self, event):
        pass


class FSR6BRCReceiver(RCReceiver):
    """An implementation of the receiver behaviors for an FS-R6B receiver.
    """

    def __init__(self, adc_lib):
        """Initializes a new FS-R6B receiver
        """
        self.adc_lib = adc_lib

        self.broadcaster = make_broadcaster()

        # Pins used for input
        self.pins = {
            "RUDDER": "P0_0",
            "TRIM": "P0_1",
            "MODE": "P0_5"
        }

    def _start_input_listening(self):
        self.adc_lib.setup()

        t = Timer(RC_READ_INTERVAL, self._read_input)
        t.start()

    def _read_input(self):
        """Reads new input values and sends them to the broadcaster."""
        input_values = {}

        for ch in self.pins:
            # According to some sources online, there is a bug in the ADC driver, so we have to read the value twice
            self.adc_lib.read(self.pins[ch])
            input_values[ch] = self.adc_lib.read(self.pins[ch])

        self.send_inputs(self.process_inputs(input_values))

    def send_inputs(self, inputs):
        """Sends inputs to the broadcaster to be published.

        Keyword arguments:
        inputs – Inputs to be sent. A dictionary with keys 'RUDDER', 'TRIM', and 'MODE'
        """
        self.broadcaster.move_rudder(degrees_starboard=inputs["RUDDER"])
        self.broadcaster.change_trim(degrees_in=inputs["TRIM"])
        self.broadcaster.change_mode(mode=inputs["MODE"])

    @staticmethod
    def process_inputs(input_values):
        """Delegates the transformation of raw input values into the correct units.

        Keyword arguments:
        inputs – Inputs to be processed. A dictionary with keys 'RUDDER', 'TRIM', and 'MODE'

        Returns:
        A new dictionary of inputs with standard units.
        """
        return {
            "RUDDER": FSR6BRCReceiver._scale_rudder_input(raw_value=input_values["RUDDER"]),
            "TRIM": FSR6BRCReceiver._scale_trim_input(raw_value=input_values["TRIM"]),
            "MODE": FSR6BRCReceiver._transform_mode(input_voltage=input_values["MODE"])
        }

    @staticmethod
    def _scale_rudder_input(raw_value=0):
        """Scales the rudder values from the raw value to degrees to starboard.

        Keyword arguments:
        raw_value -- The raw rudder input.

        Returns:
        The rudder input in degrees to starboard.
        """
        return raw_value

    @staticmethod
    def _scale_trim_input(raw_value=0):
        """Scales the trim values from the raw value to degrees in.

        Keyword arguments:
        raw_value -- The raw trim input.

        Returns:
        The trim input in degrees trimming in.
        """
        return raw_value

    @staticmethod
    def _transform_mode(input_voltage=0):
        """Maps an input voltage to a navigation mode.

        Keyword arguments:
        input_voltage -- The input voltage.

        Returns:
        The navigation mode corresponding to the input voltage.
        """
        return NavigationMode.MANUAL


def make_rc_receiver():
    """Generates the appropriate implementation of RCReceiver.

    Implements the abstract factory pattern, except calls constructors directly instead of factory methods.

    Returns:
    The correct RCReceiver for the environment.
    """
    if environ["ENV"] == "test":
        return TestableRCReceiver()
    else:
        import Adafruit_BBIO.ADC as ADC
        return FSR6BRCReceiver(ADC)
