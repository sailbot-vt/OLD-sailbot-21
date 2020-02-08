import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import numpy as np
import src.buoy_detection.Distance_Calculator as dc
import src.buoy_detection.config_reader as config_reader
import math


class DistanceCalculatorTest(unittest.TestCase):

    def setUp(self):
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.config = config_reader.get_config(self.config_filename)
        self.calc = dc.DistanceCalculator(self.config)

    def test_get_disparity_value(self):
        """Test the get_disparity_value method."""
        # Test behavior when no image is given.
        self.assertIsNone(dc.get_disparity_value(None, 1, 1))

        # Assume image is 640 x 360
        # Create fake disparity image with increasing values
        # for each pixel
        # Creates array of shape (360, 640, 1)
        # 360 and 640 are switched because cv2 uses (row, column) coordinates
        disparity_frame = np.arange(640 * 360, dtype=np.float).reshape(-1, 640)
        disparity_frame = np.expand_dims(disparity_frame, axis=2)

        # Test inside:
        test_x = 40
        test_y = 50
        near_frame = disparity_frame[test_y-1:test_y+1, test_x-1:test_x+1]
        expected_value = near_frame.sum() / near_frame.size
        self.assertAlmostEqual(dc.get_disparity_value(disparity_frame, test_x, test_y),
                               expected_value)

        # Test outside
        test_x = 639
        test_y = 50
        expected_value = disparity_frame[test_y, test_x]
        self.assertAlmostEqual(dc.get_disparity_value(disparity_frame, test_x, test_y),
                               expected_value)

    def test_get_distance(self):
        """Test the get_distance method."""

        # Test valid inputs.
        self.calc.baseline = 0.5
        self.calc.depth_map_calculator.focal_length = 1
        self.assertAlmostEqual(self.calc.get_distance(2), 0.25)

        # Test an input disparity of 0.
        self.assertEqual(self.calc.get_distance(0), math.inf)

    def test_get_bearing_from_pixel(self):
        """Test the get_bearing_from_pixel method."""

        # Test stats taken from PS3 EYE camera
        # https://www.cnet.com/products/sony-playstation-eye-camera-web-camera-series/
        self.calc.depth_map_calculator.hfov_rads = np.deg2rad(75)
        self.calc.depth_map_calculator.image_size = (640, 480)

        # Format: ((x_pixel, camera_rotation), expected_output)
        data_list = [((280, 0), 5.478814),
                     ((280, 50), 55.478814),
                     ((280, -50), -44.52119),
                     ((370, 0), -6.83683),
                     ((320, 20), 20),
                     ((320, 200), -160),
                     ((320, -200), 160)]

        for (x_pixel, camera_rotation), expected_output in data_list:
            self.assertAlmostEqual(expected_output, self.calc.get_bearing_from_pixel(x_pixel, camera_rotation), 5)
