import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import src.buoy_detection.calibration as calibration
import src.buoy_detection.config_reader as config_reader

import numpy as np


class CalibrationTests(unittest.TestCase):
    """Tests the methods in buoy_detection/calibration.py."""

    def setUp(self):
        """Initializes the configuration object so that we can easily
        make lots of Calibrator objects during testing.

        Side Effects:
            Loads in the test YAML configuration.
        """
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.config = config_reader.get_config(self.config_filename)

    @patch("src.buoy_detection.calibration.Calibrator")
    def test_load_config_and_run(self, mock_calibrator):
        """Tests the _load_config_and_run method."""
        calibration.load_config_and_run(self.config_filename)

        # Test if the Calibrator is created with the right configuration.
        mock_calibrator.assert_called_once_with(self.config)

        # Test if the run_calibration method is called with the correct output file-names.
        mock_calibrator.assert_has_calls([call().run_calibration("stereo_calibration.npz", "projection_matrices.npz")])

    """Test Calibrator methods"""

    def test_get_object_points(self):
        """Tests the Calibrator's _get_object_points method."""
        # Initialize the calibrator with some basic settings.
        calibrator = calibration.Calibrator(self.config)
        calibrator.grid_shape = (3, 4)
        calibrator.square_size = 3

        # Compare the object point method's result to what it should be,
        # given below.
        self.assertTrue(np.array_equal(
            calibrator._get_object_points(),
            np.array([
                [0, 0, 0], [3, 0, 0], [6, 0, 0],
                [0, 3, 0], [3, 3, 0], [6, 3, 0],
                [0, 6, 0], [3, 6, 0], [6, 6, 0],
                [0, 9, 0], [3, 9, 0], [6, 9, 0]
            ], np.float32)))

    def test_find_corners_fail(self):
        """Tests the Calibrator's _find_corners_fail method."""
        calibrator = calibration.Calibrator(self.config)
        calibrator.unreadable_images = set()

        # Pretend this is the path to an image with an invalid chessboard.
        broken_path = "/path/to/broken/image.png"

        calibrator._find_corners_fail(broken_path)

        # Test to see if the method successfully added the basename of the broken image
        # to the unreadable images set.
        self.assertSetEqual(calibrator.unreadable_images, {"image.png"})


