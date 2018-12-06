import unittest
from unittest.mock import MagicMock
from tests.mock_bbio import Adafruit_BBIO
from src.sail.sail_trimmer import make_sail_subscriber, SailSubscriberType
from src.sail.sail_servo_controller import SailServoController

"""Some constants in need of a home"""
pwm_pin = 1 #Need to figure out
duty_max = 0
duty_min = 0
angle_max = 180
angle_min = -180

class SailTests(unittest.TestCase):
    """Tests the methods in sail"""

    def setUp(self):
        self.sail_angles = [0,-90, 90, 180, 45, -22.5, -93]
        self.constrained_sail_angles = [0, 0, 90, 90, 45, 0, 0]
        Adafruit_BBIO.PWM.start = MagicMock(name='Adafruit_BBIO.PWM.start')
        Adafruit_BBIO.PWM.set_duty_cycle = MagicMock(name='Adafruit_BBIO.PWM.set_duty_cycle')

        self.sail_control = SailServoController(pwm_pin, duty_min, duty_max,
        angle_min, angle_max)
        self.subscriber = make_sail_subscriber(SailSubscriberType.Testable)

    def tearDown(self):
        """Return to initial conditions."""
        self.subscriber = make_sail_subscriber(SailSubscriberType.Testable)

    def test_subscriber(self):
        """Uses the mock subscriber to test the sail system"""
        Adafruit_BBIO.PWM.start.assert_called()
        Adafruit_BBIO.PWM.set_duty_cycle.assert_called()

    def test_sail_turn_to(self):
        """
        Not sure if mocking a servo would be better. It probably would as it
        would seperate the possible failure points.
        """
        for i in range(len(self.sail_angles)):
            output = self.sail_control.sail_turn_to(self.sail_angles[i])
            assert self.sail_control.current_sail_angle == self.constrained_sail_angles[i]
            assert output == self.constrained_sail_angles[i]
            Adafruit_BBIO.PWM.set_duty_cycle.assert_called()


        """
        Need to impliment check for servo output
        for angle in self.sail_angles:
            Adafruit_BBIO.PWM.assert_called_with()
        """

    def test_sail_angle_to_servo_angle(self):
        """
        Test the sail_angle_to_servo_angle method with the standard set of test
        angles.
        """
        for angle in self.sail_angles:
            assert self.sail_control.sail_angle_to_servo_angle(angle) == self.sail_control.servo.angle_min + (self.sail_control.servo.angle_max - self.sail_control.servo.angle_min) * (angle/90)

    def test_constrain_sail_angle(self):
        for i in range(len(self.sail_angles)):
            assert self.sail_control.constrain_sail_angle(self.sail_angles[i]) == self.constrained_sail_angles[i]

if __name__ == "__main__":
    unittest.main()
