import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

from numpy import sign

from src.navigation_mode import NavigationMode
from src.pin import PinType

BBB_MAX_INPUT_VOLTAGE = 1.8


class RCReceiver:
    """An implementation of the receiver behaviors for a receiver using the BBB ADC pins."""

    def __init__(self, broadcaster, pins):
        """Initializes a new ADC receiver.

        Keyword arguments:
        broadcaster -- An RC broadcaster object.
        pins -- The pin map with keys 'TRIM', 'RUDDER', 'MODE1', and 'MODE2' associated with Pin objects.

        Returns:
        A new BBIOReceiver
        """
        self.broadcaster = broadcaster
        self.pins = pins

        ADC.setup()
        GPIO.setup(pins["MODE1"], GPIO.IN)
        GPIO.setup(pins["MODE2"], GPIO.OUT)

    def read_input(self):
        """Reads new input values and sends them to the broadcaster."""
        input_values = {}

        for ch in self.pins:
            if self.pins[ch].pin_type == PinType.ADC:
                # According to sources online, there is a bug in the ADC driver, so we have to read the value twice
                ADC.read(self.pins[ch])
                input_values[ch] = ADC.read(self.pins[ch].pin_name)
            elif self.pins[ch].pin_type == PinType.GPIO:
                input_values[ch] = GPIO.input(self.pins[ch].pin_name)

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

    def _process_inputs(self, input_values):
        """Delegates the transformation of raw input values into the correct units.

        Keyword arguments:
        inputs – Inputs to be processed. A dictionary with keys 'RUDDER', 'TRIM', 'MODE1', and 'MODE2'

        Returns:
        A new dictionary of inputs with standard units.
        """
        return {
            "RUDDER": RCReceiver._scale_rudder_input(pin=self.pins["RUDDER"], raw_value=input_values["RUDDER"]),
            "TRIM": RCReceiver._scale_trim_input(pin=self.pins["TRIM"], raw_value=input_values["TRIM"]),
            "MODE": RCReceiver._transform_mode(input_voltages=(input_values["MODE1"], input_values["MODE2"]))
        }

    @staticmethod
    def _scale_rudder_input(pin, raw_value=0):
        """Scales the rudder values from the raw value to degrees to starboard.

        Preconditions:
        raw_value is on a scale of 0 to max_value.

        Keyword arguments:
        raw_value -- The raw rudder input.

        Returns:
        The rudder input in degrees to starboard.
        """
        normalized_value = RCReceiver._normalize_voltage(raw_value, pin)  # Between -1 and 1
        degrees_starboard = sign(normalized_value) * 80 * (normalized_value ** 2)  # Between -80 and 80
        return degrees_starboard

    @staticmethod
    def _scale_trim_input(pin, raw_value=0):
        """Scales the trim values from the raw value to degrees in.

        Keyword arguments:
        raw_value -- The raw trim input.

        Returns:
        The trim input in degrees trimming in.
        """
        normalized_value = RCReceiver._normalize_voltage(raw_value, pin)  # Between -1 and 1

        degrees_in = sign(normalized_value) * 20 * (normalized_value ** 2)  # Between -20 and 20
        return degrees_in

    @staticmethod
    def _transform_mode(input_voltages=(0, 0)):
        """Maps an input voltage to a navigation mode.

        Keyword arguments:
        input_voltage -- The input voltage.

        Returns:
        The navigation mode corresponding to the input voltage.
        """
        return NavigationMode.MANUAL

    @staticmethod
    def _normalize_voltage(read_value, pin):
        v_range = pin.max_v - pin.min_v
        read_v = BBB_MAX_INPUT_VOLTAGE * read_value
        shift_factor = pin.min_v
        return 2 * (((read_v - shift_factor) / v_range) - 0.5)  # Between -1 and 1

