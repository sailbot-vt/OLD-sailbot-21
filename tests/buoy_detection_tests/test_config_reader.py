import unittest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import src.buoy_detection.config_reader as config_reader


class ConfigReaderTests(unittest.TestCase):
    """Tests the functions in buoy_detection/config_reader.py"""

    def setUp(self):
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.config = \
            {"calibration": {
                "chessboard_specs": {
                    "square_size": .024,
                    "grid_shape": (6, 9)
                },
                "finding_corners": {
                    "corner_flags": "cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK | " +
                                    "cv2.CALIB_CB_ADAPTIVE_THRESH",
                    "csp_window_size": (11, 11),
                    "csp_zero_zone": (-1, -1)
                },
                "term_criteria": {
                    "term_flags": "cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER",
                    "max_iterations": 30,
                    "min_accuracy": 0.001
                },
                "rectification_alpha": 0.25,
                "draw_image": True,
                "delete_unreadable_images": False,
                "base_path": "~/test/directory/images/",
                "calibration_export_filename": "stereo_calibration.npz",
                "projection_export_filename": "projection_matrices.npz"
            }}

    def test_get_config(self):
        read_config = config_reader.get_config(self.config_filename)
        self.assertDictEqual(self.config, read_config, "Read configuration is incorrect!")

    def test_get_calibration_config(self):
        read_calibration_config = config_reader.get_calibration_config(self.config_filename)
        self.assertDictEqual(self.config["calibration"],
                             read_calibration_config, "Read calibration configuration is incorrect!")
