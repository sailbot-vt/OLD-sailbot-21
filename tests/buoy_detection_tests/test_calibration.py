import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import src.buoy_detection.calibration as calibration
import src.buoy_detection.config_reader as config_reader


class CalibrationTests(unittest.TestCase):
    """Tests the methods in buoy_detection/calibration.py."""

    def setUp(self):
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.calibration_config = config_reader.get_calibration_config(self.config_filename)

    @patch("src.buoy_detection.calibration.Calibrator")
    def test_load_config_and_run(self, mock_calibrator):
        calibration.load_config_and_run(self.config_filename)

        # Test if the Calibrator is created with the right configuration.
        mock_calibrator.assert_called_once_with(self.calibration_config)

        # Test if the run_calibration method is called with the correct output file-names.
        mock_calibrator.assert_has_calls([call().run_calibration("stereo_calibration.npz", "projection_matrices.npz")])



