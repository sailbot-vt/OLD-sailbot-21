import unittest
from unittest.mock import MagicMock
from src.sail.mainsheet import Mainsheet


class MainsheetTests(unittest.TestCase):
    """Tests the methods in rudder"""
    def setUp(self):
        self.servo = MagicMock(name="servo")
        self.servo.turn_to = MagicMock(name="servo.turn_to")
        self.mainsheet = Mainsheet(self.servo, {
            "sheeting_adv": 1,
            "max_boom_angle": 85
        })

    def test_turn_to(self):
        self.mainsheet.trim_boom_to(8)
        self.servo.turn_to.assert_called_with(-34.5)

        self.mainsheet.trim_boom_to(-70)
        self.servo.turn_to.assert_called_with(-42.5)

        self.mainsheet.trim_boom_to(80)
        self.servo.turn_to.assert_called_with(37.5)

    def test_boom_angle_to_servo_angle(self):
        self.assertEqual(self.mainsheet.boom_angle_to_servo_angle(60), 17.5)
        self.assertEqual(self.mainsheet.boom_angle_to_servo_angle(0), -42.5)

    def test_trim_in_by(self):
        self.mainsheet.trim_boom_to(0)

        self.mainsheet.trim_in_by(20)
        self.servo.turn_to.assert_called_with(-22.5)

        self.mainsheet.trim_in_by(-40)
        self.servo.turn_to.assert_called_with(-42.5)

        self.mainsheet.trim_in_by(80)
        self.servo.turn_to.assert_called_with(37.5)

        self.mainsheet.trim_in_by(30)
        self.servo.turn_to.assert_called_with(42.5)


if __name__ == "__main__":
    unittest.main()
