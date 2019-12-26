import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.kalman_filter import KalmanFilter

from pubsub import pub
from datetime import datetime as dt
import time

class KalmanFilterTests(unittest.TestCase):
    """Tests the methods in KalmanFilter"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.init_pos = [0,0]
        self.init_vel = [0,0]
        self.kalman = KalmanFilter(init_pos, init_vel)

    def test_update_trans_matrix(self, mock_now):
        """Tests the _update_trans_matrix method of KalmanFilter"""
        # check that initialized as expected
        truth_state_trans = np.eye(4)
        np.assert_allclose(self.kalman.state_trans, truth_state_trans)

        # check that delta_t is changed as expected
        truth_state_trans[0, 3] = 1
        truth_state_trans[1, 4] = 1
        self.last_time_changed = 0
        with patch('datetime.datetime.now', method.return_value = 1):
            self.kalman._update_trans_matrix()
        np.assert_allclose(self.kalman.state_trans, truth_state_trans)

        # check that delta_t is changed as expected over multiple iterations
        truth_state_trans[0, 3] = 2
        truth_state_trans[1, 4] = 2
        for n in range(1, 5, 2):
            with patch('datetime.datetime.now', method.return_value = (n+1)):
                self.kalman._update_trans_matrix()
            np.assert_allclose(self.kalman.state_trans, truth_state_trans)
