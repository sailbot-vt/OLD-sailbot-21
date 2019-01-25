from enum import Enum
from abc import ABC, abstractmethod

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO


class PinType(Enum):
    """An enum type to denote the type of pin"""
    GPIO = 0,
    ADC = 1


class Pin(ABC):
    """Holds information about a BBB pin."""

    def __init__(self, config):
        """Creates a new pin.

        Keyword arguments:
        name -- The string identifier for the pin
        type -- The pin type
        """
        self.pin_name = config["pin_name"]

    @abstractmethod
    def read(self):
        """Returns a value scaled to [-1, 1]"""
        pass


class ADCPin(Pin):
    """Provides an interface to an analog input pin"""

    MAX_INPUT_VOLTAGE = 1.8

    def __init__(self, config):
        super().__init__(config)

        self.min_v = config.get("min_v")
        self.default_v = config.get("default_v")
        self.max_v = config.get("max_v")

        ADC.setup()

    def read(self):
        """Reads the voltage being supplied to the pin.

        Returns:
        A floating-point value in [-1, 1], where -1 and 1 are min_v and max_v,
        respectively.
        """
        ADC.read(self.pin_name)  # According to the Internet, we have to do this twice
        raw_value = ADC.read(self.pin_name)
        return self._normalize_voltage(raw_value)

    def read_v(self):
        """Reads the voltage being supplied to the pin.

        Returns:
        The voltage currently being read by the pin.
        """
        ADC.read(self.pin_name)
        return ADCPin.MAX_INPUT_VOLTAGE * ADC.read(self.pin_name)

    def _normalize_voltage(self, read_value):
        v_range = self.max_v - self.min_v
        read_v = ADCPin.MAX_INPUT_VOLTAGE * read_value
        shift_factor = self.min_v
        return 2 * (((read_v - shift_factor) / v_range) - 0.5)  # Between -1 and 1


class GPIOPin(Pin):
    """Provides an interface to a GPIO pin"""
    def __init__(self, config):
        super().__init__(config)

        self._io_type = GPIO.IN

        if config["io_type"] == "OUT":
            self.io_type = GPIO.OUT
        else:
            self.io_type = GPIO.IN

    @property
    def io_type(self):
        return self._io_type

    @io_type.setter
    def io_type(self, value):
        self._io_type = value
        GPIO.setup(self.pin_name, value)

    def read(self):
        """Reads input from the pin.

        Returns:
        True if there is voltage being supplied to the pin, false otherwise.
        """
        self.io_type = GPIO.IN
        return GPIO.input(self.pin_name)

    def set_state(self, state):
        """Sets the output state of the pin.

        Keyword arguments:
        state -- Boolean, true will send out high voltage, false will send out low.
        """
        self.io_type = GPIO.OUT
        if state:
            GPIO.output(self.pin_name, GPIO.HIGH)
        else:
            GPIO.output(self.pin_name, GPIO.LOW)


def make_pin(config):
    """Method to create a new pin.

    Implements the factory design pattern.

    Keyword arguments:
    config -- A pin configuration dictionary.
        ADC pins must have min-default-max voltages specified.

    Returns:
    The type of pin specified in the config.
        """
    pin_type = PinType[config["pin_type"]]
    if pin_type == PinType.ADC:
        return ADCPin(config)
    else:
        return GPIOPin(config)
