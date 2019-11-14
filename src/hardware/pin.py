from abc import ABC
from enum import Enum

from pubsub import pub

class PinType(Enum):
    """An enum type to denote the type of pin"""
    Testable = 0,
    GPIO = 1,
    ADC = 2,
    PWM = 3,
    UART = 4


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
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = self.value, rw_state = 'r')
        return self.value

    def set_state(self, state):
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = self.value, rw_state = 'w')
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

        try:
            self.adc_lib.setup()
        except:
            pass

    def read(self):
        """Reads the voltage being supplied to the pin.

        Returns:
        A floating-point value in [-1, 1], where -1 and 1 are min_v and max_v,
        respectively.
        """
        self.adc_lib.read(
            self.pin_name)  # According to the Internet, we have to do this twice
        raw_value = self.adc_lib.read(self.pin_name)
        norm_value = self._normalize_voltage(raw_value)
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = norm_value, rw_state = 'r')
        return norm_value 
    def read_v(self):
        """Reads the voltage being supplied to the pin.

        Returns:
        The voltage currently being read by the pin.
        """
        self.adc_lib.read(self.pin_name)
        return self.adc_lib.read(self.pin_name)

    def _normalize_voltage(self, read_value):
        v_range = self.max_v - self.min_v
        read_v = read_value
        shift_factor = self.min_v
        return 2 * (((read_v - shift_factor) / v_range) - 0.5) # Between -1 and 1


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

        self.pin_name = config['pin_name']

    @property
    def io_type(self):
        return self._io_type

    @io_type.setter
    def io_type(self, value):
        self._io_type = value
        try:
            self.gpio_lib.setup(self.pin_name, value)
        except:
            pass

    def read(self):
        """Reads input from the pin.

        Returns:
        True if there is voltage being supplied to the pin, false otherwise.
        """
        self.io_type = self.gpio_lib.IN
        value = self.gpio_lib.input(self.pin_name)
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = value, rw_state = 'r')
        return value 
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
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = state, rw_state = 'w')

class PWMPin(Pin):
    """Provides an interface to a PWM pin"""

    def __init__(self, config, pwm_lib):
        super().__init__(config)
        self.pwm_lib = pwm_lib
        
        self.pin_name = config['pin_name']

    def start(self, duty, frequency=60.0):
        self.pwm_lib.start(self.pin_name, duty, frequency)
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = 'PWM_start', rw_state = 'w')

    def stop(self):
        self.pwm_lib.stop(self.pin_name)
        pub.sendMessage("write msg", pin_name = self.pin_name, msg = 'PWM_stop', rw_state = 'w')

    def set_duty_cycle(self, duty_cycle):
        self.pwm_lib.set_duty_cycle(self.pin_name, duty_cycle)

    def set_frequency(self, duty_cycle):
        self.pwm_lib.set_frequency(self.pin_name, duty_cycle)


class UARTPin(Pin):
    """Provides an interface to a UART pin"""

    def __init__(self, config, uart_lib):
        super().__init__(config)
        self.channel = config["channel"]
        self.uart_lib = uart_lib

    def setup(self):
        """ Set up and start the UART channel. 
        
        This will export the given UART so that it can be 
        accessed by other software that controls its serial lines.

        Keyword arguments:
        channel -- UART channel to set up. 
                One of "UART1", "UART2", "UART4" or "UART5"
        """
        self.uart_lib.setup(self.channel)

    def cleanup(self):
        """ Cleans up the UART"""
        # self.uart_lib.cleanup()
        # Above code apparently causes kernal panic
        pass


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
            return GPIOPin(config, GPIO)
        return GPIOPin(config, mock_lib)
    elif pin_type == PinType.PWM:
        if mock_lib is None:
            import Adafruit_BBIO.PWM as PWM
            return PWMPin(config, PWM)
        return PWMPin(config, mock_lib)
    elif pin_type == PinType.UART:
        if mock_lib is None:
            import Adafruit_BBIO.UART as UART
            return UARTPin(config, UART)
        return UARTPin(config, mock_lib)
    else:
        return TestablePin(name=config["pin_name"],
                           read_value=config.get("read_value") or 0)
