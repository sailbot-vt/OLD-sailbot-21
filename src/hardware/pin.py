from enum import Enum
from abc import ABC, abstractmethod


class PinType(Enum):
    """An enum type to denote the type of pin"""
    Testable = 0,
    GPIO = 1,
    ADC = 2


class Pin(ABC):
    """Holds information about a BBB pin."""

    def __init__(self, config):
        """Creates a new pin.

        Keyword arguments:
        name -- The string identifier for the pin
        type -- The pin type
        """
        self.pin_name = config["pin_name"]


class TestablePin(Pin):
    """Provides a Pin object to be used for testing."""
    def __init__(self, name, read_value):
        self.pin_name = name
        self.value = read_value
        self.written_values = []

    def read(self):
        return self.value

    def set_state(self, state):
        self.written_values.append(state)

    def start(self, *args):
        pass

    def stop(self):
        pass

    def set_duty_cycle(self, value):
        self.written_values.append(value)

    def set_frequency(self, value):
        self.written_values.append(value)


class ADCPin(Pin):
    """Provides an interface to an analog input pin"""

    MAX_INPUT_VOLTAGE = 1.8

    def __init__(self, config, adc_lib):
        super().__init__(config)

        self.min_v = config.get("min_v")
        self.default_v = config.get("default_v")
        self.max_v = config.get("max_v")

        self.adc_lib = adc_lib

        self.adc_lib.setup()

    def read(self):
        """Reads the voltage being supplied to the pin.

        Returns:
        A floating-point value in [-1, 1], where -1 and 1 are min_v and max_v,
        respectively.
        """
        self.adc_lib.read(self.pin_name)  # According to the Internet, we have to do this twice
        raw_value = self.adc_lib.read(self.pin_name)
        return self._normalize_voltage(raw_value)

    def read_v(self):
        """Reads the voltage being supplied to the pin.

        Returns:
        The voltage currently being read by the pin.
        """
        self.adc_lib.read(self.pin_name)
        return ADCPin.MAX_INPUT_VOLTAGE * self.adc_lib.read(self.pin_name)

    def _normalize_voltage(self, read_value):
        v_range = self.max_v - self.min_v
        read_v = ADCPin.MAX_INPUT_VOLTAGE * read_value
        shift_factor = self.min_v
        return 2 * (((read_v - shift_factor) / v_range) - 0.5)  # Between -1 and 1


class GPIOPin(Pin):
    """Provides an interface to a GPIO pin"""
    def __init__(self, config, gpio_lib):
        super().__init__(config)

        self.gpio_lib = gpio_lib

        self._io_type = gpio_lib.IN

        if config["io_type"] == "OUT":
            self.io_type = gpio_lib.OUT
        else:
            self.io_type = gpio_lib.IN

    @property
    def io_type(self):
        return self._io_type

    @io_type.setter
    def io_type(self, value):
        self._io_type = value
        self.gpio_lib.setup(self.pin_name, value)

    def read(self):
        """Reads input from the pin.

        Returns:
        True if there is voltage being supplied to the pin, false otherwise.
        """
        self.io_type = self.gpio_lib.IN
        return self.gpio_lib.input(self.pin_name)

    def set_state(self, state):
        """Sets the output state of the pin.

        Keyword arguments:
        state -- Boolean, true will send out high voltage, false will send out low.
        """
        self.io_type = self.gpio_lib.OUT
        if state:
            self.gpio_lib.output(self.pin_name, self.gpio_lib.HIGH)
        else:
            self.gpio_lib.output(self.pin_name, self.gpio_lib.LOW)


class PWMPin(Pin):
    """Provides an interface to a PWM pin"""
    def __init__(self, config, pwm_lib):
        super().__init__(config)
        self.pwm_lib = pwm_lib

    def start(self, duty, frequency=60.0):
        self.pwm_lib.start(self.pin_name, duty, frequency)

    def stop(self):
        self.pwm_lib.stop(self.pin_name)

    def set_duty_cycle(self, duty_cycle):
        self.pwm_lib.set_duty_cycle(self.pin_name, duty_cycle)

    def set_frequency(self, duty_cycle):
        self.pwm_lib.set_frequency(self.pin_name, duty_cycle)


def make_pin(config, mock_lib=None):
    """Method to create a new pin.

    Implements the factory design pattern.

    Keyword arguments:
    config -- A pin configuration dictionary.
        ADC pins must have min-default-max voltages specified.

    Returns:
    The type of pin specified in the config.
    """
    pin_type = PinType[config.get("pin_type") or "Testable"]
    if pin_type == PinType.ADC:
        if mock_lib is None:
            import Adafruit_BBIO.ADC as ADC
            return ADCPin(config, ADC)
        return ADCPin(config, mock_lib)
    elif pin_type == PinType.GPIO:
        if mock_lib is None:
            import Adafruit_BBIO.GPIO as GPIO
            return ADCPin(config, GPIO)
        return GPIOPin(config, mock_lib)
    else:
        return TestablePin(name=config["pin_name"],
                           read_value=config.get("read_value") or 0)
