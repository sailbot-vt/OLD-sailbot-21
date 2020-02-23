import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.kalman_filter import KalmanFilter

import numpy as np
from datetime import datetime as dt
import time

class KalmanFilterTests(unittest.TestCase):
    """Tests the methods in KalmanFilter"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.init_pos = [0.,0.]
        self.init_vel = [0.,0.]
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
        # check if correct functions calls are made with correct arguments
        with patch('src.tracking.kalman_filter.kalman.update') as mock_update:

            # mock return values for update
            state = self.kalman.state
            covar = self.kalman.covar
            mock_update.return_value = (state, covar)

            # generate measurement values (arbitrary)
            pos, vel = np.array([4, 45]), np.array([1, 90])

            measurement = np.append(pos, vel)

            # generate new measurement covar
            measurement_covar = self.kalman.measurement_covar

            # call update
            self.kalman.update(pos, vel)

            # check for proper behavior
            self.assertEqual(1, mock_update.call_count)
            call_args = mock_update.call_args
            np.testing.assert_allclose(self.kalman.state, call_args[1]['x'])
            np.testing.assert_allclose(self.kalman.covar, call_args[1]['P'])
            np.testing.assert_allclose(measurement, call_args[1]['z'])
            np.testing.assert_allclose(measurement_covar, call_args[1]['R'])
            np.testing.assert_allclose(self.kalman.measurement_trans, call_args[1]['H'])

        # check if kalman filter results correctly

        # set up measurement values, expected results
        measurements = np.array([[0, 0, 5, -5],
                                 [1, 1, -2.5, 2.5],
                                 [2.5, 0, 0, 3],
                                 [-1.5, -4.75, 2, 2]])

        updated_states = np.array([[0, 0, 2.5, -2.5],
                                 [0.5, 0.5, 0, 0],
                                 [1.5, 0.25, 0, 1.5],
                                 [0, -2.25, 1, 1.75]])

        
        # loop thru different values for state
        for ii in range(np.size(measurements, 0)):

            # reset covariance matrix
            pos_sigma, vel_sigma = np.array([1, 1]), np.array([2, 2])
            self.kalman.covar = np.diag(np.append(pos_sigma, vel_sigma))
            self.kalman.measurement_covar = self.kalman.covar

            # call update
            hist_score = 1
            self.kalman.update(measurements[ii, 0:2], measurements[ii, 2:4])
        
            # check if updated state is close to expected
            updated_state = updated_states[ii]
            np.testing.assert_allclose(updated_state, self.kalman.state)

    @patch('src.tracking.kalman_filter.KalmanFilter._update_trans_matrix')
    @patch('src.tracking.kalman_filter.KalmanFilter._update_process_noise')
    def test_predict(self, mock_update_noise, mock_update_trans):
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
            self.assertEqual(1, mock_predict.call_count)
            call_args = mock_predict.call_args
            np.testing.assert_allclose(self.kalman.state, call_args[1]['x'])
            np.testing.assert_allclose(self.kalman.covar, call_args[1]['P'])
            np.testing.assert_allclose(self.kalman.state_trans, call_args[1]['F'])
            np.testing.assert_allclose(np.eye(self.kalman.covar.shape[0]), call_args[1]['Q'])        # since calc process noise is mocked 

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

        # loop thru different values for state
        for ii in range(np.size(states, 0)):
            # set kalman state
            self.kalman.state = states[ii]

            # call predict
            self.kalman.predict()
        
            # check if predicted state is close to expected
            predicted_state = predicted_states[ii]
            np.testing.assert_allclose(predicted_state, self.kalman.state)

    def test_update_process_noise(self):
        """Tests update process noise method"""
        # set delta_t
        dt = 2
        self.kalman.delta_t = dt

        # generate list of ranges
        rng_list = [1.0, 4.0, 25.0, 100.0]

        # generate list of velocities
        vel_list = [(1., 1.), (2., 4.), (10., 5.)]

        # iterate through values
        for rng, vel in zip(rng_list, vel_list):
            # set kalman state
            self.kalman.state = np.array([rng, 0, vel[0], vel[1]])

            # calculate process noise values
            process_noise_truth = np.diag(np.ones(4))
            rng_noise_fac = dt * (1 + vel[0])
            bearing_noise_fac = dt * (1 + vel[1]) * (0.5 + 50*(np.power(rng, -2)))
            process_noise_truth[0::2, 0::2] *= rng_noise_fac
            process_noise_truth[1::2, 1::2] *= bearing_noise_fac

            # call update process noise
            self.kalman._update_process_noise()

            # check for correct behavior
            np.testing.assert_almost_equal(process_noise_truth, self.kalman.process_noise)

    def test_adjust_wraparound(self):
        """Tests adjust wraparound method"""
        # generate bearing data
        bearing_list = [0, 45, 120., 179.99, 180.00001, 185, 250, 323, 355.23, 359.999]
        adjust_bearing_list = [0, 45, 120., 179.99, -179.99999, -175, -110, -37, -4.77, -0.001]

        # loop through values
        for bearing, adjusted_bearing in zip(bearing_list, adjust_bearing_list):
            # store bearing in kalman state
            self.kalman.state[1] = bearing

            # call adjust wraparound
            self.kalman._adjust_wraparound()

            truth_state = np.array([0., adjusted_bearing, 0., 0.]).astype(np.float32)

            # check for correct behavior
            np.testing.assert_allclose(truth_state, self.kalman.state, atol=1e-4)
