import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import src.buoy_detection.Depth_Map_Calculator as dmc
import src.buoy_detection.config_reader as config_reader
import cv2


class DepthMapCalculatorTests(unittest.TestCase):
    """Tests the methods in src/buoy_detection/Depth_Map_Calculator.py"""

    def setUp(self):
        """Set up DepthMap and load configs/images for testing."""
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.config = config_reader.get_config(self.config_filename)
        self.calc = dmc.DepthMap(self.config)
        self.base_dir = "./tests/buoy_detection_tests/calibration_images/"
        self.left_dir = self.base_dir + "LEFT/"
        self.right_dir = self.base_dir + "RIGHT/"

        self.left_img = cv2.imread(self.left_dir + "image1.jpg")
        self.right_img = cv2.imread(self.right_dir + "image1.jpg")

    def test_calculate_depth_map(self):
        """Test the calculate_depth_map method."""
        self.calc.get_left_camera_image = MagicMock(return_value=self.left_img)
        self.calc.get_right_camera_image = MagicMock(return_value=self.right_img)

        # Test valid image pair

        self.calc.left = MagicMock(grab=MagicMock(return_value=True))
        self.calc.right = MagicMock(grab=MagicMock(return_value=True))
        result = self.calc.calculate_depth_map()

        # Use weird loop instead of assertNotEqual because unittest doesn't like
        # me comparing matrices to (None, None).
        for element in result:
            self.assertIsNotNone(element)

        # Test bad image pair

        self.calc.left.grab = MagicMock(return_value=False)
        self.calc.right.grab = MagicMock(return_value=False)
        self.assertEqual(self.calc.calculate_depth_map(), (None, None))

    def test_get_left_camera_image(self):
        """Tests the get_left_camera_image method."""
        # Test bad grab
        self.calc.left = MagicMock(grab=MagicMock(return_value=False))
        self.assertIsNone(self.calc.get_left_camera_image())

        # Test valid grab
        self.calc.left = MagicMock(grab=MagicMock(return_value=True),
                                   retrieve=MagicMock(return_value=(True, self.left_img)))
        self.assertIsNotNone(self.calc.get_left_camera_image())

    def test_get_right_camera_image(self):
        """Tests the get_right_camera_image method."""
        # Test bad grab
        self.calc.right = MagicMock(grab=MagicMock(return_value=False))
        self.assertIsNone(self.calc.get_right_camera_image())

        # Test valid grab
        self.calc.right = MagicMock(grab=MagicMock(return_value=True),
                                    retrieve=MagicMock(return_value=(True, self.right_img)))
        self.assertIsNotNone(self.calc.get_right_camera_image())
