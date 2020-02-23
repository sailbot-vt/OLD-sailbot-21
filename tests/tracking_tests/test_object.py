import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.object import Object

import numpy as np
import time

class ObjectTests(unittest.TestCase):
    """Tests the methods in Object"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.object = Object(0, 0)      # empty object

    def test_set_object_state(self):
        """Tests set object state method of Object"""
        # set kalman state to arbitrary choice of numbers
        rb = [2, 45]
        rb_prime = [5, 5]
        self.object.kalman.state = np.array(rb + rb_prime)

        # call set object state method
        self.object._set_object_state()

        # ensure that object state is set correctly
        rng, bearing = rb
        rngRate, bearingRate = rb_prime

        self.assertAlmostEqual(self.object.rng, rng)
        self.assertAlmostEqual(self.object.bearing, bearing)
        self.assertAlmostEqual(self.object.rngRate, rngRate)
        self.assertAlmostEqual(self.object.bearingRate, bearingRate)

    @patch('src.tracking.object.time_in_millis')
    def test_find_object_rngRate(self, mock_time_in_millis):
        """Tests find object rngRate method of Object"""
        # set rng, time_in_millis, and lastSeen to arbitrary values
        rng = 10.
        lastSeen = 0
        millis_time = 1000
        self.object.rng = rng 
        self.object.lastSeen = lastSeen
        mock_time_in_millis.return_value = millis_time

        # call find object rngRate method
        self.object._find_object_rngRate()

        # ensure that return value is correct
        rngRate = 1000. * (rng - 0) / (millis_time - lastSeen)

        self.assertAlmostEqual(rngRate, self.object.rngRate)

    @patch('src.tracking.object.time_in_millis')
    def test_find_object_bearringRate(self, mock_time_in_millis):
        """Tests find object bearingRate method of Object"""
        # set bearing, time_in_millis, and lastSeen to arbitrary values
        bearing = 5.
        lastSeen = 0
        millis_time = 1000
        self.object.bearing = bearing 
        self.object.lastSeen = lastSeen
        mock_time_in_millis.return_value = millis_time

        # call find object rngRate method
        self.object._find_object_bearingRate()

        # ensure that return value is correct
        bearingRate = 1000. * (bearing - 0) / (millis_time - lastSeen)

        self.assertAlmostEqual(bearingRate, self.object.bearingRate)

    @patch('src.tracking.object.time_in_millis')
    @patch('src.tracking.object.Object._find_object_bearingRate')
    @patch('src.tracking.object.Object._find_object_rngRate')
    @patch('src.tracking.object.Object._set_object_state')
    @patch('src.tracking.object.KalmanFilter.update')
    def test_update(self, mock_kalman_update, mock_set_obj_state, mock_find_rngRate,
                          mock_find_bearingRate, mock_time_in_millis):
        """Tests update method of Object"""
        # set mocks and states to arbitrary values for testing
        rng, bearing = 2, 3
        rngRate, bearingRate = 0, 0
        self.object.rngRate, self.object.bearingRate = rngRate, bearingRate
        kalman_state = np.array([rng, bearing, 0, 0])
        self.object.kalman.state = kalman_state         # used by _set_object_state
        
        time_in_millis_val = 5
        mock_time_in_millis.return_value = time_in_millis_val

        # call update
        self.object.update(rng, bearing)

        # hist score (with one detection in hist)
#        max_val, min_val = 1.05, 0.95
#        scale_fac = (max_val - min_val) / self.object.histLength
#        hist_score = max_val - ((1+4.5)*scale_fac)

        # ensure proper behavior
        mock_kalman_update.assert_called_with([rng, bearing], [rngRate, bearingRate])

        mock_set_obj_state.assert_called_once_with()
        mock_find_rngRate.assert_called_once_with()
        mock_find_bearingRate.assert_called_once_with()

        self.assertEqual(time_in_millis_val, self.object.lastSeen)
        
        # check update history behavior
        truth_history = [None] * self.object.histLength
        truth_history[0] = 1
        self.assertEqual(truth_history, self.object.updateHist)

        # repeat test with non-None rngRate and bearingRate

        # reset all mocks
        mock_kalman_update.reset_mock()
        mock_set_obj_state.reset_mock()
        mock_find_rngRate.reset_mock()
        mock_find_bearingRate.reset_mock()
        mock_time_in_millis.reset_mock()

        # set mocks and states to arbitrary values for testing
        rng, bearing = 2, 3
        rngRate, bearingRate = 5, 90
        kalman_state = np.array([rng, bearing, rngRate, bearingRate])
        self.object.kalman.state = kalman_state         # used by _set_object_state
        
        time_in_millis_val = 5
        mock_time_in_millis.return_value = time_in_millis_val

        # call update
        self.object.update(rng, bearing, rngRate, bearingRate)

        # hist score (with two detections in hist)
#        hist_score = max_val - ((2+4)*scale_fac)

        # ensure proper behavior
        mock_kalman_update.assert_called_with([rng, bearing], [rngRate, bearingRate])

        mock_set_obj_state.assert_called_once_with()
        mock_find_rngRate.assert_called_once_with()
        mock_find_bearingRate.assert_called_once_with()

        self.assertEqual(time_in_millis_val, self.object.lastSeen)

        # check update history behavior
        truth_history[1] = 1
        self.assertEqual(truth_history, self.object.updateHist)

        # repeat test with None for rng and bearing (object not seen case)

        # reset all mocks
        mock_kalman_update.reset_mock()
        mock_set_obj_state.reset_mock()
        mock_find_rngRate.reset_mock()
        mock_find_bearingRate.reset_mock()
        mock_time_in_millis.reset_mock()

        # call update
        self.object.update(None, None)

        # ensure proper behavior
        mock_kalman_update.assert_not_called()

        mock_set_obj_state.assert_not_called()
        mock_find_rngRate.assert_not_called()
        mock_find_bearingRate.assert_not_called()

        # check update history behavior
        truth_history[0:3] = [0, 1, 1]
        self.assertEqual(truth_history, self.object.updateHist)

    @patch('src.tracking.object.Object._set_object_state')
    @patch('src.tracking.object.KalmanFilter.predict')
    def test_predict(self, mock_predict, mock_set_obj_state):
        """Tests predict method of Object"""
        # call predict
        self.object.predict()

        # ensure proper calls are made
        mock_predict.assert_called_once_with()
        mock_set_obj_state.assert_called_once_with()

    def test_calc_hist_score(self):
        """Tests calc history score method of object"""
        # set up hist vals and scores
        update_hist_vals = [[1, None, None, None, None, None, None, None, None, None],
                            [0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        hist_len = 10.
        max_val = 1.
        min_val = 0.
        scale_fac = (max_val - min_val) / hist_len

        # check for correct behavior
        for hist_vals in update_hist_vals:
            # calc hist score
            num_nones = sum(el is None for el in hist_vals)
            truth_hist_score = (sum(filter(None, hist_vals)) + (0.5 * num_nones)) * scale_fac

            # set update hist
            self.object.updateHist = hist_vals

            # call calc hist score
            self.object._calc_hist_score()

            # check for correct behavior
            self.assertAlmostEqual(truth_hist_score, self.object.histScore)

    @patch('src.tracking.object.np.sum')
    def test_calc_confidence(self, mock_sum):
        """Tests calc confidence method"""
        # generate vals
        hist_vals = [1., 0.9, 0., 0.75, 0]
        sum_vals = [0., 20., 50., 100., 150.]

        truth_confidence_vals = [1., 0.85, 0.25, 0.375, 0.]

        # iterate through values
        for hist_val, sum_val, truth_confidence in zip(hist_vals, sum_vals, truth_confidence_vals):
            # set hist score
            self.object.histScore = hist_val

            # set mock val
            mock_sum.return_value = sum_val

            # call calc confidence
            self.object._calc_confidence()

            # check for correct behavior
            self.assertAlmostEqual(truth_confidence, self.object.confidence)
