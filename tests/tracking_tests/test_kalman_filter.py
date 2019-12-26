import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.kalman_filter import KalmanFilter

import numpy as np
from pubsub import pub
from datetime import datetime as dt
import time

#TODO REMOVE
import pdb

class KalmanFilterTests(unittest.TestCase):
    """Tests the methods in KalmanFilter"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.init_pos = [0,0]
        self.init_vel = [0,0]
        self.kalman = KalmanFilter(self.init_pos, self.init_vel)

    @patch('src.tracking.kalman_filter.time_in_millis')
    def test_update_trans_matrix(self, mock_time_in_millis):
        """Tests the _update_trans_matrix method of KalmanFilter"""
        # check that initialized as expected
        truth_state_trans = np.eye(4)
        np.testing.assert_allclose(self.kalman.state_trans, truth_state_trans)

        # check that delta_t is changed as expected
        truth_state_trans[0, 2] = 1
        truth_state_trans[1, 3] = 1
        self.kalman.last_time_changed = 0
        mock_time_in_millis.return_value = 1

        self.kalman._update_trans_matrix()
        np.testing.assert_allclose(self.kalman.state_trans, truth_state_trans)

        # check that delta_t is changed as expected over multiple iterations
        truth_state_trans[0, 2] = 2
        truth_state_trans[1, 3] = 2

        for n in range(3, 7, 2):
            mock_time_in_millis.return_value = n
            self.kalman._update_trans_matrix()

            np.testing.assert_allclose(self.kalman.state_trans, truth_state_trans)
