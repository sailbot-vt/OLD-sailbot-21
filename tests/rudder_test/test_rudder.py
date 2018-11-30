import unittest
from unittest.mock import MagicMock
from tests.mock_pwm import Adafruit_BBIO
from src.rudder.rudder_driver import make_rudder_subscriber, RudderSubscriberType
from src.rudder.rudder_servo_controller import RudderServoController

"""Some constants in need of a home"""
pwm_pin = 1 #Need to figure out
duty_max = 0
duty_min = 0
angle_max = 180
angle_min = -180
mechanical_advantage = 1


class RudderTests(unittest.TestCase):
    """Tests the methods in rudder"""

    def setUp(self):
        self.rudder_angles = [0,-90, 90, 180, 45, -22.5, -93]
        self.constrained_rudder_angles = [0,-90, 90, 90, 45, -22.5, -90]
        Adafruit_BBIO.PWM.start = MagicMock(name='Adafruit_BBIO.PWM.start')
        Adafruit_BBIO.PWM.set_duty_cycle = MagicMock(name='Adafruit_BBIO.PWM.set_duty_cycle')

        self.rudder_control = RudderServoController(pwm_pin, duty_min, duty_max,
        angle_min, angle_max, mechanical_advantage)
        self.subscriber = make_rudder_subscriber(RudderSubscriberType.Testable)

    def tearDown(self):
        """Return to initial conditions."""
        self.subscriber = make_rudder_subscriber(RudderSubscriberType.Testable)

    def test_subscriber(self):
        """Uses the mock subscriber to test the rudder system"""
        Adafruit_BBIO.PWM.start.assert_called()
        Adafruit_BBIO.PWM.set_duty_cycle.assert_called()

    def test_rudder_turn_to(self):
        """
        Not sure if mocking a servo would be better. It probably would as it
        would seperate the possible failure points.
        """
        for i in range(len(self.rudder_angles)):
            output = self.rudder_control.rudder_turn_to(self.rudder_angles[i])
            assert self.rudder_control.current_rudder_angle == self.constrained_rudder_angles[i]
            assert output == self.constrained_rudder_angles[i]
            Adafruit_BBIO.PWM.assert_called()


        """
        Need to impliment check for servo output
        for angle in self.rudder_angles:
            Adafruit_BBIO.PWM.assert_called_with()
        """

    def test_rudder_angle_to_servo_angle(self):
        """
        Test the rudder_angle_to_servo_angle method with the standard set of test
        angles.
        """
        for angle in self.rudder_angles:
            assert self.rudder_control.rudder_angle_to_servo_angle(angle) == angle*self.rudder_control.mechanical_advantage

    def test_constrain_rudder_angle(self):
        for angle in self.rudder_angles:
            assert angle * self.rudder_control.mechanical_advantage <= self.rudder_control.angle_max
            assert angle * self.rudder_control.mechanical_advantage >= self.rudder_control.ngle_min

if __name__ == "__main__":
    unittest.main()
