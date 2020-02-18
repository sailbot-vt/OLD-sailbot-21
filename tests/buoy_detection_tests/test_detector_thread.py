import unittest
try:
    from unittest.mock import MagicMock, patch, call
except ImportError:
    from mock import MagicMock, patch, call

import numpy as np
import cv2

import src.buoy_detection.detector_thread as detector_thread
import src.buoy_detection.config_reader as config_reader


class DetectorThreadTests(unittest.TestCase):
    """Tests the methods in src/buoy_detection/detector_thread.py"""

    def setUp(self):
        self.config_filename = "./tests/buoy_detection_tests/test_config.yaml"
        self.config = config_reader.get_config(self.config_filename)

        # Set `boat` parameter in constructor to None since it's
        # not used yet (as of 2/16/20)
        self.thread = detector_thread.DetectorThread(self.config, None)

    def test_find_object_centers(self):
        """Test the find_object_centers method."""
        mask = np.zeros((480, 640), dtype=np.uint8)

        # Generate fake detections.
        mask[10:21, 20:31] = 255
        mask[350:401, 360:411] = 255

        # Write the centers of mass of each detection (x, y)
        # Note that above, the mask areas were marked as [y, x] since
        # the images are in row-major order (first index is the row).
        center1 = (25, 15)
        center2 = (385, 375)

        # Find contours.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        returned_centers = detector_thread.find_object_centers(contours)

        self.assertTrue(center1 in returned_centers)
        self.assertTrue(center2 in returned_centers)

    def test_stretch_bounds(self):
        """Test the stretch_bounds method."""
        self.assertEqual([3, 7], detector_thread.stretch_bounds([3, 5], 7))
        self.assertEqual([-56, 5], detector_thread.stretch_bounds([3, 5], -56))
        self.assertEqual([3, 5], detector_thread.stretch_bounds([3, 5], 5))

    def test_get_camera_heading(self):
        """Test the get_camera_heading method.
        get_camera_heading isn't implemented yet, so we just have
        a placeholder test here."""
        self.assertEqual(0, self.thread.get_camera_heading())

    @patch('pubsub.pub.sendMessage')
    def test_handle_contours(self, mock_send_msg):
        """Test the handle_contours method."""
        disparity_frame = np.zeros((480, 640), dtype=np.uint8)

        # Give a list of no contours. No message should have been sent.
        self.thread.handle_contours([], disparity_frame)
        mock_send_msg.assert_not_called()

        # Give a list of two contours. One message should have been sent
        # with two detections.
        mask = np.zeros((480, 640), dtype=np.uint8)
        mask[100:140, 100:140] = 255
        mask[200:240, 200:240] = 255

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.thread.handle_contours(contours, disparity_frame)

        # Test that one message was sent with two detections.
        # We want the first call to mock_send_msg ([0]),
        # the kwargs to that call (3rd element of the call tuple, or [2]), and
        # the epoch_frame kwarg (['epoch_frame']).
        # The epoch_frame should contain two detections.
        self.assertEqual(2, len(mock_send_msg.mock_calls[0][2]['epoch_frame']))

    def test_run(self):
        """Test main runner method."""
        # TODO Finish.
