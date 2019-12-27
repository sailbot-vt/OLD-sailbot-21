import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.tracking.object import Object

from src.utils.coord_conv import cartesian_to_polar, polar_to_cartesian

import numpy as np
import time

#TODO REMOVE
import pdb

class ObjectTests(unittest.TestCase):
    """Tests the methods in Object"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.object = Object(0, 0)      # empty object

    def test_set_object_state(self):
        """Tests set object state method of Object"""
        # set kalman state to arbitrary choice of numbers
        xy = [2, 2]
        xy_prime = [5, 5]
        self.object.kalman.state = np.array(xy + xy_prime)

        # call set object state method
        self.object._set_object_state()

        # ensure that object state is set correctly
        rng, bearing = cartesian_to_polar(xy[0], xy[1])
        rngRate, bearingRate = cartesian_to_polar(xy_prime[0], xy_prime[1])

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

    @patch('src.tracking.object.polar_to_cartesian')
    def test_get_cart_position(self, mock_polar_to_cart):
        """Tests get cartesian position method of Object"""
        # set rng and bearing to arbitrary numbers
        rng = 5
        self.object.rng = rng
        bearing = 6
        self.object.bearing = bearing

        # call _get_cart_position
        self.object._get_cart_position()

        # check if polar_to_cartesian is called with correct values
        mock_polar_to_cart.assert_called_with(rng, bearing)

    @patch('src.tracking.object.polar_to_cartesian')
    def test_get_cart_velocity(self, mock_polar_to_cart):
        """Tests get cartesian position method of Object"""
        # set rng and bearing to arbitrary numbers
        rngRate = 5
        self.object.rngRate = rngRate
        bearingRate = 6
        self.object.bearingRate = bearingRate

        # call _get_cart_position
        self.object._get_cart_velocity()

        # check if polar_to_cartesian is called with correct values
        mock_polar_to_cart.assert_called_with(rngRate, bearingRate)

    @patch('src.tracking.object.polar_to_cartesian')
    @patch('src.tracking.object.time_in_millis')
    @patch('src.tracking.object.Object._find_object_bearingRate')
    @patch('src.tracking.object.Object._find_object_rngRate')
    @patch('src.tracking.object.Object._set_object_state')
    @patch('src.tracking.object.Object._get_cart_velocity')
    @patch('src.tracking.object.KalmanFilter.update')
    def test_update(self, mock_kalman_update, mock_get_cart_vel, mock_set_obj_state, mock_find_rngRate,
                          mock_find_bearingRate, mock_time_in_millis, mock_polar_to_cart):
        """Tests update moethod of Object"""
        # set mocks and states to arbitrary values for testing
        update_cart_vel = polar_to_cartesian(5, 90)
        mock_get_cart_vel.return_value = update_cart_vel

        rng, bearing = 2, 3
        kalman_state = np.array([rng, bearing, 0, 5])
        self.object.kalman.state = kalman_state         # used by _set_object_state
        
        time_in_millis_val = 5
        mock_time_in_millis.return_value = time_in_millis_val

        polar_to_cart_val = (2,2)
        mock_polar_to_cart.return_value = polar_to_cart_val

        # call update
        self.object.update(4, 45)    # arguments do not impact values (since we are mocking everything)

        # ensure proper behavior
        mock_kalman_update.assert_called_with(*polar_to_cart_val, *update_cart_vel)

        mock_set_obj_state.assert_called_once_with()
        mock_find_rngRate.assert_called_once_with()
        mock_find_bearingRate.assert_called_once_with()

        self.assertEqual(time_in_millis_val, self.object.lastSeen)

        # repeat test with non-None rngRate and bearingRate

        # reset all mocks
        mock_kalman_update.reset_mock()
        mock_get_cart_vel.reset_mock()
        mock_set_obj_state.reset_mock()
        mock_find_rngRate.reset_mock()
        mock_find_bearingRate.reset_mock()
        mock_time_in_millis.reset_mock()
        mock_polar_to_cart.reset_mock()

        # set mocks and states to arbitrary values for testing
        rng, bearing = 2, 3
        kalman_state = np.array([rng, bearing, 0, 5])
        self.object.kalman.state = kalman_state         # used by _set_object_state
        
        time_in_millis_val = 5
        mock_time_in_millis.return_value = time_in_millis_val

        polar_to_cart_val = (2,2)
        mock_polar_to_cart.return_value = polar_to_cart_val

        # call update
        self.object.update(4, 45, 4, 45)    # arguments do not impact values (since we are mocking everything)

        # ensure proper behavior
        mock_kalman_update.assert_called_with(*polar_to_cart_val, *polar_to_cart_val)

        mock_set_obj_state.assert_called_once_with()
        mock_find_rngRate.assert_called_once_with()
        mock_find_bearingRate.assert_called_once_with()

        self.assertEqual(time_in_millis_val, self.object.lastSeen)

    @patch('src.tracking.object.Object._set_object_state')
    @patch('src.tracking.object.KalmanFilter.predict')
    def test_predict(self, mock_predict, mock_set_obj_state):
        """Tests predict method of Object"""
        # call predict
        self.object.predict()

        # ensure proper calls are made
        mock_predict.assert_called_once_with()
        mock_set_obj_state.assert_called_once_with()
