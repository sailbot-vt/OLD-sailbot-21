import unittest
from unittest.mock import MagicMock

from src.rudder.rudder import Rudder


class RudderTests(unittest.TestCase):
    """Tests the methods in rudder"""
    def setUp(self):
        self.servo = MagicMock(name="servo")
        self.servo.turn_to = MagicMock(name="servo.turn_to")
        self.rudder = Rudder(self.servo, {
            "mechanical_adv": 1,
            "full_port_angle": -70,
            "full_starboard_angle": 70
        })

    def test_turn_to(self):
        self.rudder.turn_to(8)
        self.servo.turn_to.assert_called_with(8)

        self.rudder.turn_to(-70)
        self.servo.turn_to.assert_called_with(-70)

        self.rudder.turn_to(80)
        self.servo.turn_to.assert_called_with(70)

    def test_rudder_angle_to_servo_angle(self):
        assert self.rudder.rudder_angle_to_servo_angle(60) == 60
        assert self.rudder.rudder_angle_to_servo_angle(-10) == -10

    def test_change_rudder_angle(self):
        self.rudder.turn_to(0)

        self.rudder.change_rudder_angle(20)
        self.servo.turn_to.assert_called_with(20)

        self.rudder.change_rudder_angle(-40)
        self.servo.turn_to.assert_called_with(-20)

        self.rudder.change_rudder_angle(80)
        self.servo.turn_to.assert_called_with(60)

        self.rudder.change_rudder_angle(30)
        self.servo.turn_to.assert_called_with(70)


if __name__ == "__main__":
    unittest.main()
