import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.rudder.rudder import Rudder

class RudderTests(unittest.TestCase):
    """Tests the methods in rudder"""
    def setUp(self):
        self.rudder = Rudder({
            "mechanical_adv": 1,
            "full_port_angle": -70,
            "full_starboard_angle": 70
        })

    @patch('src.rudder.rudder.pub', autospec=True)
    def test_turn_to(self, mock_pub):
        in_angle_values = [8, -70, 80]
        out_angle_values = [8, -70, 70]
        for in_ang, truth_ang in zip(in_angle_values, out_angle_values):
            self.rudder.turn_to(in_ang)
            mock_pub.sendMessage.assert_any_call("turn rudder to", rudder_ang=truth_ang)
        
    @patch('src.rudder.rudder.pub', autospec=True)
    def test_rudder_angle_to_servo_angle(self, mock_pub):
        assert self.rudder.rudder_angle_to_servo_angle(60) == 60
        assert self.rudder.rudder_angle_to_servo_angle(-10) == -10

    @patch('src.rudder.rudder.pub', autospec=True)
    def test_change_rudder_angle(self, mock_pub):
        in_angle_values = [0, 20, -40, 80, 30]
        out_angle_values = [0, 20, -20, 60, 70]
        for in_ang, truth_ang in zip(in_angle_values, out_angle_values):
            self.rudder.change_rudder_angle(in_ang)
            mock_pub.sendMessage.assert_any_call("turn rudder to", rudder_ang=truth_ang)

if __name__ == "__main__":
    unittest.main()
