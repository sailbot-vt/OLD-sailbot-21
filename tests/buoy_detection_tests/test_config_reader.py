import unittest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import src.buoy_detection.config_reader as config_reader


class ConfigReaderTests(unittest.TestCase):
    """Tests the functions in buoy_detection/config_reader.py"""

    def setUp(self):
        self.config_filename = "./tests/buoy_detection_tests/test_reader_config.yaml"
        self.config = \
            {
                "common": {
                    "baseline": 0.2
                },

                "calibration": {
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
                },

                "depth_map": {
                    "calibration_filename": "stereo_calibration.npz",
                    "fov": 56,
                    "camera_numbers": (2, 3),
                    "draw_image": False,
                    "stereo_bm": {
                        "min_disparity": 0,
                        "num_disparities": 160,
                        "block_size": 5,
                        "uniqueness_ratio": 15,
                        "speckle_window_size": 0,
                        "speckle_range": 2,
                        "remap_interpolation": "cv2.INTER_LINEAR",
                        "depth_visualization_scale": 32
                    }
                }}

    def test_get_config(self):
        """Ensures the get_config method behaves as expected."""
        read_config = config_reader.get_config(self.config_filename)
        self.assertDictEqual(self.config, read_config, "Read configuration is incorrect!")