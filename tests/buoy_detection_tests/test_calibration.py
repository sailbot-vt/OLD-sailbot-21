import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import src.buoy_detection.calibration as calibration
import src.buoy_detection.config_reader as config_reader

import numpy as np
import os
import shutil


def write_to_new_file(filename, msg):
    """Helper function to let us easily create
    small files for testing.
    """
    with open(filename, 'w') as fd:
        fd.write(msg)


class CalibrationTests(unittest.TestCase):
    """Tests the methods in buoy_detection/calibration.py.
    REQUIRES a sample set of L/R pictures in
    ./tests/buoy_detection_tests/calibration_images.
    Sample test set taken from:
    https://github.com/sourishg/stereo-calibration/tree/master/calib_imgs/1
    (29 pairs of images, 640x360)
    """
    def setUp(self):
        """Initializes the configuration object so that we can easily
        make lots of Calibrator objects during testing.

        Side Effects:
            Loads in the test YAML configuration.
        """
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.config = config_reader.get_config(self.config_filename)
        self.calibrator = calibration.Calibrator(self.config)
        self.out_file1 = "./tests/buoy_detection_tests/out_file1.npz"
        self.out_file2 = "./tests/buoy_detection_tests/out_file2.npz"

        # Create mock image directory
        self.mock_base_dir = "./tests/buoy_detection_tests/images/"
        self.mock_left_dir = self.mock_base_dir + "LEFT/"
        self.mock_right_dir = self.mock_base_dir + "RIGHT/"

    def tearDown(self):
        """Clean up created files and objects!"""
        if os.path.isfile(self.out_file1):
            os.remove(self.out_file1)

        if os.path.isfile(self.out_file2):
            os.remove(self.out_file2)

        if os.path.isdir(self.mock_base_dir):
            shutil.rmtree(self.mock_base_dir)

    @patch("src.buoy_detection.calibration.Calibrator")
    def test_load_config_and_run(self, mock_calibrator):
        """Tests the _load_config_and_run method."""
        calibration.load_config_and_run(self.config_filename)

        # Test if the Calibrator is created with the right configuration.
        mock_calibrator.assert_called_once_with(self.config)

    """Test Calibrator methods"""

    def test_run_calibration(self):
        """Test run_calibration method."""
        self.calibrator.delete_unreadable_images = False  # Just in case it gets set True in the config.

        self.calibrator.run_calibration(self.out_file1, self.out_file2)

        # Assert output files are successfully created.
        self.assertTrue(os.path.isfile(self.out_file1) and os.path.isfile(self.out_file2))

    def test_get_object_points(self):
        """Tests the Calibrator's _get_object_points method."""
        # Initialize the calibrator with some basic settings.
        self.calibrator.grid_shape = (3, 4)
        self.calibrator.square_size = 3

        # Compare the object point method's result to what it should be,
        # given below.
        self.assertTrue(np.array_equal(
            self.calibrator._get_object_points(),
            np.array([
                [0, 0, 0], [3, 0, 0], [6, 0, 0],
                [0, 3, 0], [3, 3, 0], [6, 3, 0],
                [0, 6, 0], [3, 6, 0], [6, 6, 0],
                [0, 9, 0], [3, 9, 0], [6, 9, 0]
            ], np.float32)))

    def test_find_chessboards(self):
        """Tests the _find_chessboards method."""
        image_points_l, image_points_r, camera_size = self.calibrator._find_chessboards()
        num_valid_test_images = 29
        self.assertEqual(len(image_points_l), num_valid_test_images)
        self.assertEqual(len(image_points_r), num_valid_test_images)
        self.assertEqual(camera_size, (640, 360))

    def test_remove_unreadable_image_pairs(self):
        """Tests the _remove_unreadable_image_pairs method."""

        os.mkdir(self.mock_base_dir)
        os.mkdir(self.mock_left_dir)
        os.mkdir(self.mock_right_dir)
        for i in range(0, 2):
            write_to_new_file(self.mock_left_dir + "image" + str(i), "data")
            write_to_new_file(self.mock_right_dir + "image" + str(i), "data")

        self.calibrator.delete_unreadable_images = True
        self.calibrator.left_camera_directory = self.mock_left_dir
        self.calibrator.right_camera_directory = self.mock_right_dir
        self.calibrator.unreadable_images = ["image0", "image999"]

        # First test: Does it successfully handle an image that doesn't
        # even exist? ("image999")
        self.calibrator._remove_unreadable_image_pairs()

        # Check to see "image0" is gone and "image1" is still present.
        self.assertFalse(os.path.isfile(self.mock_left_dir + "image0") or
                         os.path.isfile(self.mock_right_dir + "image0"))
        self.assertTrue(os.path.isfile(self.mock_left_dir + "image1") and
                        os.path.isfile(self.mock_right_dir + "image1"))

    def test_find_corners_fail(self):
        """Tests the Calibrator's _find_corners_fail method."""
        self.calibrator.unreadable_images = set()

        # Pretend this is the path to an image with an invalid chessboard.
        broken_path = "/path/to/broken/image.png"

        self.calibrator._find_corners_fail(broken_path)

        # Test to see if the method successfully added the basename of the broken image
        # to the unreadable images set.
        self.assertSetEqual(self.calibrator.unreadable_images, {"image.png"})


