import unittest

from src.hardware.pin import make_pin
from src.hardware.servo import Servo


class PinTests(unittest.TestCase):
    """Tests methods of the Pin family."""
    def setUp(self):
        self.pin = make_pin({
            "pin_name": "Hello"
        })
        self.servo = Servo(self.pin, {
            "full_left_duty": 1,
            "full_right_duty": 2,
            "full_left_angle": -180,  # The 360 degree servo
            "full_right_angle": 180
        })

    def test_calc_duty_cycle(self):
        val = self.servo.calc_duty_cycle(-180)
        assert val == 100
        val = self.servo.calc_duty_cycle(180)
        assert val == 98
        val = self.servo.calc_duty_cycle(0)
        assert val == 99

    def test_turn_to(self):
        self.servo.turn_to(90)
        assert self.servo.current_angle == 90
        # The servo turns to 0 on instantiation, so index starts at 1
        assert self.pin.written_values[1] == 98.5

        self.servo.turn_to(-90)
        assert self.servo.current_angle == -90
        assert self.pin.written_values[2] == 99.5

        self.servo.turn_to(4000)
        assert self.servo.current_angle == 180
        assert self.pin.written_values[3] == 98


if __name__ == "__main__":
    unittest.main()
