import os
import unittest

from src.autonomy.events.config_reader import read_interval

class EventsConfigReaderTests(unittest.TestCase):
    """Tests methods in Events Config Reader"""
    def setUp(self):
        """Sets up the path of config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_interval(self):
        """Tests read interval method of config reader"""
        event_type = 'fleet_race'
        nav_int = 5

        self.assertEqual(nav_int, read_interval(event_type))
