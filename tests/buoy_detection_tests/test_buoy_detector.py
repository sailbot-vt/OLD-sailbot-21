import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import src.buoy_detection.buoy_detector as bd
import numpy as np
import pickle
import os


class BuoyDetectorTests(unittest.TestCase):
    """Tests the methods in src/buoy_detection/buoy_detector.py."""

    TEST_HISTOGRAM_PATH = "./tests/buoy_detection_tests/histogram.pickle"

    def tearDown(self):
        """Clean up after each test."""

        # Remove the testing histogram, if it was created.
        if os.path.isfile(BuoyDetectorTests.TEST_HISTOGRAM_PATH):
            os.remove(BuoyDetectorTests.TEST_HISTOGRAM_PATH)

    def test_get_mask(self):
        """Test that the get_mask method successfully completes
        and returns a mask of the correct size."""

        input_image = np.random.rand(480, 640)
        mask = bd.get_mask(input_image, 0.6, 2, 12)

        self.assertEqual(mask.shape, (480, 640))

    def test_clean_mask(self):
        """Test that basic opening and closing operations on a mask
        work."""

        # Create test image and set top half to black...
        input_image = np.zeros((480, 640), np.uint8)

        # ... and set bottom half of image to white.
        input_image[:, 320:] = 255

        # Add specks of the opposite color on each side.
        input_image[2, 2] = 255
        input_image[477, 637] = 0

        output_image = bd.clean_mask(input_image, 2, 12)

        # Test if the specks were removed.
        self.assertEqual(output_image[2, 2], 0)
        self.assertEqual(output_image[477, 637], 255)
        self.assertEqual(output_image.shape, (480, 640))

    def test_map_func_combined(self):
        """Test the map_func_combined method."""
        test_histogram = np.random.rand(180, 256, 256)
        result = bd.map_func_combined((1, 2, 3), test_histogram)

        self.assertEqual(result, test_histogram[1, 2, 3])

    def test_get_relevance_map(self):
        """Test the get_relevance_map method to ensure it
        successfully completes and returns a relevance map matrix
        of the correct size."""
        test_hsv = np.random.randint(0, 100, (480, 640, 3))  # 3 channels for HSV
        test_histogram = np.random.rand(180, 256, 256)
        output_map = bd.get_relevance_map(test_hsv, test_histogram, 7)

        self.assertEqual((480, 640), output_map.shape)

    def test_get_histogram(self):
        """Test the get_histogram method."""

        # Dump a test histogram in the test folder.
        test_histogram = np.random.rand(180, 256, 256)
        with open(BuoyDetectorTests.TEST_HISTOGRAM_PATH, 'wb') as pickle_file:
            pickle.dump((test_histogram,), pickle_file)

        # See if we can retrieve it with get_histogram.
        retrieved = bd.get_histogram(BuoyDetectorTests.TEST_HISTOGRAM_PATH)
        self.assertTrue(np.array_equal(test_histogram, retrieved))

    def test_process_image(self):
        """Test the process_image method to ensure it
        successfully completes and returns a relevance map matrix
        and mask matrix of the correct size."""
        image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)  # Random BGR image
        threshold = 0.8
        histogram_3d = np.random.rand(180, 256, 256)
        open_radius = 2
        close_radius = 12
        blur_ksize = 7

        relevance_map, mask = bd.process_image(image, threshold, histogram_3d,
                                               open_radius, close_radius, blur_ksize)

        self.assertEqual((480, 640), relevance_map.shape)
        self.assertEqual((480, 640), mask.shape)
