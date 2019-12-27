import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.kalman_filter import KalmanFilter

import numpy as np
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
        mock_time_in_millis.return_value = 1000

        self.kalman._update_trans_matrix()
        np.testing.assert_allclose(self.kalman.state_trans, truth_state_trans)

        # check that delta_t is changed as expected over multiple iterations
        truth_state_trans[0, 2] = 2
        truth_state_trans[1, 3] = 2

        for n in range(3, 7, 2):
            mock_time_in_millis.return_value = (n * 1000)
            self.kalman._update_trans_matrix()

            np.testing.assert_allclose(self.kalman.state_trans, truth_state_trans)

    def test_update(self):
        """Tests update method of kalman filter"""
        # Testing methodology:
        #   check if correct function calls are made with correct argument
        #   check if kalman filter results correctly

    @patch('src.tracking.kalman_filter.KalmanFilter._update_trans_matrix')
    def test_predict(self, mock_update_trans):
        """Tests predict method of kalman filter"""
        # Testing methodology:
        #   check if correct function calls are made with correct arguments
        #   check if kalman filter results correctly
        
        # check if correct functions calls are made with correct arguments
        with patch('src.tracking.kalman_filter.kalman.predict') as mock_predict:

            # mock return values for predict
            state = self.kalman.state
            covar = self.kalman.covar
            mock_predict.return_value = (state, covar)
            
            # call predict
            self.kalman.predict()

            # check for proper behavior
            mock_update_trans.assert_called_once_with()
            mock_predict.assert_called_once_with(x=self.kalman.state, P=self.kalman.covar, F=self.kalman.state_trans, Q=0)

        # check if kalman filter results  correctly

        # set up transition matrix
        self.kalman.state_trans[0, 2] = 1
        self.kalman.state_trans[1, 3] = 1

        # set up state values, expected results
        states = np.array([[0, 0, 5, -5],
                           [1, 1, -1, -1],
                           [-2, 0, 0, 3],
                           [-3, -5, 2, 2]])

        predicted_states = np.array([[5, -5, 5, -5],
                                     [0, 0, -1, -1],
                                     [-2, 3, 0, 3],
                                     [-1, -3, 2, 2]])

        # get covar matrix
        covar = self.kalman.covar
        
        # loop thru different values for state
        for ii in range(np.size(states, 0)):
            # set kalman state
            self.kalman.state = states[ii]

            # call predict
            self.kalman.predict()
        
            # check if predicted state is close to expected
            predicted_state = predicted_states[ii]
            np.testing.assert_allclose(predicted_state, self.kalman.state)
