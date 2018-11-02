from abc import ABC, abstractmethod
from enum import Enum

from numpy import sign

from src.navigation_mode import NavigationMode
from src.rc_input.rc_broadcaster import make_broadcaster

BBB_MAX_INPUT_VOLTAGE = 1.8
INPUT_PIN_MAX_VOLTAGE = 1.8  # Should be lower than BBB_MAX_INPUT_VOLTAGE to reduce risk to the BBB


class RCReceiverType(Enum):
    """Semantically represents a type of RCReceiver."""
    Testable = 0
    ADC = 1


class RCReceiver(ABC):
    """Defines an RCReceiver type"""
    @abstractmethod
    def read_input(self):
        pass


class TestableRCReceiver(RCReceiver):
    """A mock RCReceiver to test consumers of RCReceiver."""
    def fake_read_input(self, event):
        pass


class ADCReceiver(RCReceiver):
    """An implementation of the receiver behaviors for a receiver using the BBB ADC pins."""

    def __init__(self, broadcaster, adc_lib, pins):
        """Initializes a new FS-R6B receiver."""
        self.adc_lib = adc_lib
        self.broadcaster = broadcaster
        self.pins = pins

        self.adc_lib.setup()

    def read_input(self):
        """Reads new input values and sends them to the broadcaster."""
        input_values = {}

        for ch in self.pins:
            # According to some sources online, there is a bug in the ADC driver, so we have to read the value twice
            self.adc_lib.read(self.pins[ch])
            input_values[ch] = self.adc_lib.read(self.pins[ch])

        self._send_inputs(self._process_inputs(input_values))

    def _send_inputs(self, inputs):
        """Sends inputs to the broadcaster to be published.

        Keyword arguments:
        inputs – Inputs to be sent. A dictionary with keys 'RUDDER', 'TRIM', and 'MODE'
        """
        if "RUDDER" in inputs:
            self.broadcaster.move_rudder(degrees_starboard=inputs["RUDDER"])
        if "TRIM" in inputs:
            self.broadcaster.change_trim(degrees_in=inputs["TRIM"])
        if "MODE" in inputs:
            self.broadcaster.change_mode(mode=inputs["MODE"])

    @staticmethod
    def _process_inputs(input_values):
        """Delegates the transformation of raw input values into the correct units.

        Keyword arguments:
        inputs – Inputs to be processed. A dictionary with keys 'RUDDER', 'TRIM', and 'MODE'

        Returns:
        A new dictionary of inputs with standard units.
        """
        return {
            "RUDDER": ADCReceiver._scale_rudder_input(raw_value=input_values["RUDDER"]),
            "TRIM": ADCReceiver._scale_trim_input(raw_value=input_values["TRIM"]),
            "MODE": ADCReceiver._transform_mode(input_voltage=input_values["MODE"])
        }

    @staticmethod
    def _scale_rudder_input(raw_value=0):
        """Scales the rudder values from the raw value to degrees to starboard.

        Preconditions:
        raw_value is on a scale of 0 to max_value.

        Keyword arguments:
        raw_value -- The raw rudder input.

        Returns:
        The rudder input in degrees to starboard.
        """
        normalized_value = ADCReceiver._normalize_voltage(raw_value)  # Between -1 and 1
        degrees_starboard = sign(normalized_value) * 80 * (normalized_value ** 2)  # Between -80 and 80
        return degrees_starboard

    @staticmethod
    def _scale_trim_input(raw_value=0):
        """Scales the trim values from the raw value to degrees in.

        Keyword arguments:
        raw_value -- The raw trim input.

        Returns:
        The trim input in degrees trimming in.
        """
        normalized_value = ADCReceiver._normalize_voltage(raw_value)  # Between -1 and 1

        degrees_in = sign(normalized_value) * 20 * (normalized_value ** 2)  # Between -20 and 20
        return degrees_in

    @staticmethod
    def _transform_mode(input_voltage=0):
        """Maps an input voltage to a navigation mode.

        Keyword arguments:
        input_voltage -- The input voltage.

        Returns:
        The navigation mode corresponding to the input voltage.
        """
        return NavigationMode.MANUAL

    @staticmethod
    def _normalize_voltage(read_value, max_value=INPUT_PIN_MAX_VOLTAGE / BBB_MAX_INPUT_VOLTAGE):
        return 2 * ((read_value / max_value) - 0.5)  # Between -1 and 1


def make_rc_receiver(receiver_type=RCReceiverType.ADC, broadcaster=make_broadcaster()):
    """Generates the appropriate implementation of RCReceiver.

    Implements the factory design pattern.

    Keyword arguments:
    receiver_type -- The type of receiver to create

    Returns:
    An instance of the specified type of RCReceiver.
    """
    if receiver_type == RCReceiverType.ADC:
        import Adafruit_BBIO.ADC as ADC
        return ADCReceiver(broadcaster, ADC, {
            "RUDDER": "P0_0",
            "TRIM": "P0_1",
            "MODE": "P0_5"
        })

    return TestableRCReceiver()
