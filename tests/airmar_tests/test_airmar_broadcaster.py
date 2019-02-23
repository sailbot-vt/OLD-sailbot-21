import unittest
from unittest.mock import patch, MagicMock

from src.airmar.airmar_broadcaster import AirmarBroadcasterType
from src.airmar.airmar_broadcaster import make_broadcaster

class AirmarBroadcasterTest(unittest.TestCase):
    """ Test cases for Airmar Broadcaster """
    def setUp(self):
        pass

    @patch('src.airmar.airmar_broadcaster.pub', autospec=True)
    def test_messenger(self, mock_pub):
        """ Tests airmar messenger methods. """
        broadcaster = make_broadcaster(AirmarBroadcasterType.Messenger)
        
        # Read none
        broadcaster.read_wind_speed()
        broadcaster.read_wind_heading()
        broadcaster.read_boat_latitude()
        broadcaster.read_boat_longitude()
        broadcaster.read_boat_heading()
        broadcaster.read_boat_speed()
        mock_pub.sendMessage.assert_not_called()

        # Read value
        broadcaster.read_wind_speed(wind_speed=10.0)
        broadcaster.read_wind_heading(wind_head=10.0)
        broadcaster.read_boat_latitude(boat_lat=10.0)
        broadcaster.read_boat_longitude(boat_long=10.0)
        broadcaster.read_boat_heading(boat_head=10.0)
        broadcaster.read_boat_speed(boat_speed=10.0)

        for i in range(6):
            self.assertAlmostEqual(10.0, mock_pub.method_calls[i][2]["msgData"], 1)