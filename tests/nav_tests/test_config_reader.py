import os
import unittest

from src.autonomy.nav.config_reader import read_nav_config, read_interval

class NavConfigReaderTests(unittest.TestCase):
    """Tests methods in Nav Config Reader"""
    def setUp(self):
        """Sets up the path of config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_nav_config(self):
        """Tests read nav config method"""
        # expected values
        expected_vals = {'return_home': True, 'mark_width': 1}

        self.assertDictEqual(expected_vals, read_nav_config(self.path))

    def test_read_interval(self):
        """Tests read interval method"""
        # expected values
        expected_val = 5

        self.assertEqual(expected_val, read_interval(self.path))
