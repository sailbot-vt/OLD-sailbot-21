import os
import unittest

from src.autonomy.feature_extraction.config_reader import read_start_gate_config, read_round_buoy_config

class FeatureExtractionConfigReaderTests(unittest.TestCase):
    """Tests methods in Feature Extraction Config Reader"""
    def setUp(self):
        """Sets up the path of config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_start_gate_config(self):
        """Tests read start gate config method"""
        # expected values
        expected_vals = {'width': 5, 'width_variance': 1.5}

        self.assertDictEqual(expected_vals, read_start_gate_config(self.path))

    def test_read_round_buoy_config(self):
        """Tests read round buoy config method"""
        # expected values
        expected_vals = {'margin': 1.5}

        self.assertDictEqual(expected_vals, read_round_buoy_config(self.path))
