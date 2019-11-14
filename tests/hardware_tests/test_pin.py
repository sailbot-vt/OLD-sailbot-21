import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.hardware.pin import make_pin, ADCPin
from tests.mock_bbio import Adafruit_BBIO


class PinTests(unittest.TestCase):
    """Tests methods of the Pin family."""

    @staticmethod
    def test_gpio_read():
        """Tests that GPIOPin reads correctly."""
        # Set up the pin
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')
        gpio_pin = make_pin({
            "pin_name": "Hello",
            "pin_type": "GPIO",
            "io_type": "IN"
        }, mock_lib=Adafruit_BBIO.GPIO)

        # Fake HIGH voltage
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input',
                                             return_value=True)
        assert gpio_pin.read()

        # Fake LOW voltage
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input',
                                             return_value=False)
        assert not gpio_pin.read()


    @staticmethod
    def test_gpio_set_state():
        """Tests that GPIOPin writes correctly."""
        # Set up the pin
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.output = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.HIGH = MagicMock(name='Adafruit.BBIO.GPIO.HIGH')
        Adafruit_BBIO.GPIO.LOW = MagicMock(name='Adafruit.BBIO.GPIO.LOW')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')
        Adafruit_BBIO.GPIO.OUT = MagicMock(name='Adafruit.BBIO.GPIO.OUT')
        gpio_pin = make_pin({
            "pin_name": "Hello",
            "pin_type": "GPIO",
            "io_type": "OUT"
        }, mock_lib=Adafruit_BBIO.GPIO)

        # Set to HIGH voltage
        gpio_pin.set_state(True)
        Adafruit_BBIO.GPIO.output.assert_called_with("Hello", Adafruit_BBIO.GPIO.HIGH)

        # Set to LOW voltage
        gpio_pin.set_state(False)
        Adafruit_BBIO.GPIO.output.assert_called_with("Hello", Adafruit_BBIO.GPIO.LOW)

    @patch('src.hardware.pin.pub', autospec=True)
    def test_gpio_logger(self, mock_pub):
        """Tests that GPIOPin logs messages"""

        # Set up the pin
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')
        gpio_pin = make_pin({
            "pin_name": "GPIOread",
            "pin_type": "GPIO",
            "io_type": "IN"
        }, mock_lib=Adafruit_BBIO.GPIO)

        # Fake HIGH voltage
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input',
                                             return_value=True)

        gpio_pin.read()
        mock_pub.sendMessage.assert_any_call("write msg", pin_name="GPIOread", msg=True, rw_state='r')        

        # Set up pin for output
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.output = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.HIGH = MagicMock(name='Adafruit.BBIO.GPIO.HIGH')
        Adafruit_BBIO.GPIO.LOW = MagicMock(name='Adafruit.BBIO.GPIO.LOW')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')
        Adafruit_BBIO.GPIO.OUT = MagicMock(name='Adafruit.BBIO.GPIO.OUT')
        gpio_pin = make_pin({
            "pin_name": "GPIOwrite",
            "pin_type": "GPIO",
            "io_type": "OUT"
        }, mock_lib=Adafruit_BBIO.GPIO)

        # Set to HIGH voltage
        gpio_pin.set_state(True)
        
        mock_pub.sendMessage.assert_any_call("write msg", pin_name = "GPIOwrite", msg=True, rw_state = 'w')

    @staticmethod
    def test_adc_read_v():
        # Set up the pin
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.GPIO.setup', return_value=0.9)
        adc_pin = make_pin({
            "pin_name": "Hello",
            "pin_type": "ADC",
            "min_v": 0,
            "default_v": 0.9,
            "max_v": 1.8
        }, mock_lib=Adafruit_BBIO.ADC)

        # Tests the method
        assert abs(adc_pin.read_v() - 0.9) < 0.01

    @staticmethod
    def test_adc_read():
        # Set up the pin
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit.BBIO.ADC.read')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=(ADCPin.MAX_INPUT_VOLTAGE))
        adc_pin = make_pin({
            "pin_name": "Hello",
            "pin_type": "ADC",
            "min_v": 0,
            "default_v": 0.9,
            "max_v": 1.8
        }, mock_lib=Adafruit_BBIO.ADC)

        # Tests the method
        val = adc_pin.read()
        err = abs(val - 1)
        assert err < 0.01

        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=(0.5 * ADCPin.MAX_INPUT_VOLTAGE))

        val = adc_pin.read()
        err = abs(val - 0)
        assert err < 0.01

        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=0)

        val = adc_pin.read()
        err = abs(val + 1)
        assert err < 0.01

    
    @patch('src.hardware.pin.pub', autospec=True)
    def test_adc_logger(self, mock_pub):
        """Tests that ADCPin logs messages"""

        # Set up the pin
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit.BBIO.ADC.read')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=(ADCPin.MAX_INPUT_VOLTAGE))
        adc_pin = make_pin({
            "pin_name": "Hello",
            "pin_type": "ADC",
            "min_v": 0,
            "default_v": 0.9,
            "max_v": 1.8
        }, mock_lib=Adafruit_BBIO.ADC)

        # Tests the method
        val = adc_pin.read()
        err = abs(val - 1)
        assert err < 0.01

        mock_pub.sendMessage.assert_any_call("write msg", pin_name="Hello", msg=val, rw_state='r')        

    @staticmethod
    def test_uart_setup():
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit.BBIO.UART.setup')

        uart_pin = make_pin({
            "pin_name": "uart-test",
            "pin_type": "UART",
            "channel": "test-channel"
        }, mock_lib=Adafruit_BBIO.UART)

        # Tests the method
        uart_pin.setup()
        Adafruit_BBIO.UART.setup.assert_called_with("test-channel")

if __name__ == "__main__":
    unittest.main()
