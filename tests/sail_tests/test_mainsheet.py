import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.sail.mainsheet import Mainsheet

class MainsheetTests(unittest.TestCase):
    """Tests the methods in rudder"""
    def setUp(self):
        self.mainsheet = Mainsheet(config={
            "sheeting_adv": 1,
            "max_boom_angle": 85
        })

    @patch('src.sail.mainsheet.pub', autospec=True)
    def test_trim_boom_to(self, mock_pub):
        in_angle_values = [8, -70, 80] 
        out_angle_values = [-34.5, -42.5, 37.5] 
        for in_ang, truth_ang in zip(in_angle_values, out_angle_values):
            self.mainsheet.trim_boom_to(in_ang)
            mock_pub.sendMessage.assert_any_call("turn sail to", sail_ang=truth_ang)

    @patch('src.sail.mainsheet.pub', autospec=True)
    def test_trim_in_by(self, mock_pub):
        in_angle_values = [20, -40, 80, 30] 
        out_angle_values = [-22.5, -42.5, 37.5, 42.5] 
        self.mainsheet.trim_boom_to(0)
        for in_ang, truth_ang in zip(in_angle_values, out_angle_values):
            self.mainsheet.trim_in_by(in_ang)
            mock_pub.sendMessage.assert_any_call("turn sail to", sail_ang=truth_ang)

    def test_boom_angle_to_motor_angle(self):
        self.assertEqual(self.mainsheet.boom_angle_to_motor_angle(60), 17.5)
        self.assertEqual(self.mainsheet.boom_angle_to_motor_angle(0), -42.5)

if __name__ == "__main__":
    unittest.main()
