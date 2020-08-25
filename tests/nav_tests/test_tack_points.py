import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import numpy as np

from src.utils.coord_conv import cartesian_to_polar

from src.autonomy.nav.tack_points import place_tacks, find_beating_bounds, must_tack 

class TackPointsTests(unittest.TestCase):
    """Tests the methods in Tack Points"""
    def setUp(self):
        pass

    def test_must_tack(self):
        """Tests must tack method"""
        # set up mock boat and wind
        mock_boat = MagicMock(name = 'boat')
        mock_boat.upwind_angle = 35

        mock_wind = MagicMock(name = 'wind')

        # generate test values
        rel_angs = [0, 15, 35, 45, -15, -35, -45]

        # generate truth values
        truth_vals = [True, True, False, False, True, False, False]

        # check for correct behavior
        for rel_ang, truth_val in zip(rel_angs, truth_vals):
            mock_wind.angle_relative_to_wind.return_value = rel_ang
            self.assertEqual(truth_val, must_tack([None, None], mock_boat, mock_wind))

    def test_find_beating_bounds(self):
        """Tests find beating bounds method"""
        # generate test upwind_dists, upwind angs, strategies
        test_upwind_dists = [1, 1, 1, 1, 2]
        test_upwind_angs = [45, 45, 45, 30, 45]
        test_strategies = [0, 1, -0.5, 0, 0]

        # generate truth beating bounds
        truth_l_bounds = [-1/8., 1/4., -5/16., -1/8. * np.sqrt(3)/3., -1/4.]
        truth_r_bounds = [1/8., 1/2., -1/16., 1/8. * np.sqrt(3)/3., 1/4.]

        # check for correct behavior
        for truth_l_bound, truth_r_bound, upwind_dist, upwind_ang, strat in \
            zip(truth_l_bounds, truth_r_bounds, test_upwind_dists, test_upwind_angs, test_strategies):

            ret_l_bound, ret_r_bound = find_beating_bounds(upwind_dist, upwind_ang, strat)
            self.assertAlmostEqual(truth_l_bound, ret_l_bound, places=3)
            self.assertAlmostEqual(truth_r_bound, ret_r_bound, places=3)

    @patch('src.autonomy.nav.tack_points.find_beating_bounds')
    @patch('src.autonomy.nav.tack_points.must_tack')
    def test_place_tacks(self, mock_must_tack, mock_bounds):
        """Tests place tacks method"""
        # ---------------------------------------------------------
        # Testing methodology
        #   Test 1: no tacks needed
        #   Test 2: one tack needed (first tacking to starboard) (even strategy)
        #   Test 3: one tack needed (first tacking to port) (even strategy)
        #   Test 4: one tack needed (first tacking to port) (starboard favored strategy)
        #   Test 5: twelve tacks needed (first tacking to starboard) (even strategy)
        # ---------------------------------------------------------
        # set up mock boat, wind, config
        mock_boat = MagicMock(name = 'boat')
        mock_boat.upwind_angle = 35
        mock_wind = MagicMock(name = 'wind')
        config = {'max_tacks': 20}

        # set up waypoint
        waypoint = (20, 45)

        # -------------------------
        # Test 1 -- no tacks needed 
        # -------------------------
        mock_must_tack.return_value = False

        self.assertListEqual([], place_tacks(waypoint, mock_boat, mock_wind, config))

        # -------------------------------------------
        # Test 2 -- one tack needed (starboard first)
        # -------------------------------------------
        mock_must_tack.return_value = True
        mock_wind.distance_upwind.side_effect = [20, 10]
        rel_wind_ang = 45
        mock_wind.angle_relative_to_wind.return_value = rel_wind_ang
        mock_boat.upwind_angle = 45

        l_bound, r_bound = (-10, 10)
        mock_bounds.return_value = l_bound, r_bound

        tacks_cart = [(r_bound, r_bound),]
        tacks = [cartesian_to_polar(x, y) for (x, y) in tacks_cart]
        tacks = [(rng, bearing + waypoint[1]) for (rng, bearing) in tacks]

        np.testing.assert_almost_equal(tacks,  place_tacks(waypoint, mock_boat, mock_wind, config))

        # -------------------------------------------
        # Test 3 -- one tack needed (port first)
        # -------------------------------------------
        mock_must_tack.return_value = True
        mock_wind.distance_upwind.side_effect = [20, 10]
        rel_wind_ang = -45
        mock_wind.angle_relative_to_wind.return_value = rel_wind_ang
        mock_boat.upwind_angle = 45

        l_bound, r_bound = (-10, 10)
        mock_bounds.return_value = l_bound, r_bound

        tacks_cart = [(np.fabs(l_bound), l_bound),]
        tacks = [cartesian_to_polar(x, y) for (x, y) in tacks_cart]
        tacks = [(rng, bearing + waypoint[1]) for (rng, bearing) in tacks]

        np.testing.assert_almost_equal(tacks,  place_tacks(waypoint, mock_boat, mock_wind, config))

        # -----------------------------------------------------------------------------------
        # Test 4 -- one tack needed (first tacking to starboard) (starboard favored strategy)
        # -----------------------------------------------------------------------------------
        mock_must_tack.return_value = True
        mock_wind.distance_upwind.side_effect = [20, 2.5]
        rel_wind_ang = 45
        mock_wind.angle_relative_to_wind.return_value = rel_wind_ang
        mock_boat.upwind_angle = 45

        l_bound, r_bound = (-2.5, 17.5)
        mock_bounds.return_value = l_bound, r_bound

        tacks_cart = [(r_bound, r_bound),]
        tacks = [cartesian_to_polar(x, y) for (x, y) in tacks_cart]
        tacks = [(rng, bearing + waypoint[1]) for (rng, bearing) in tacks]

        np.testing.assert_almost_equal(tacks,  place_tacks(waypoint, mock_boat, mock_wind, config))
        
        # ----------------------------------------------------------------
        # Test 5: twelve tacks needed (first tacking to starboard) (even strategy)
        # ----------------------------------------------------------------
        mock_must_tack.return_value = True
        upwind_dists = [20,] + [20 - 5/6. - (n * 5/3.) for n in range(12)]
        mock_wind.distance_upwind.side_effect = upwind_dists
        rel_wind_ang = 65
        mock_wind.angle_relative_to_wind.return_value = rel_wind_ang
        mock_boat.upwind_angle = 30

        l_bound, r_bound = [-5 * np.sqrt(3)/6., 5 * np.sqrt(3)/6.]
        mock_bounds.return_value = l_bound, r_bound

        tacks_cart = [(5/6., r_bound), (15/6., l_bound), (25/6., r_bound), \
                      (35/6., l_bound), (45/6., r_bound), (55/6., l_bound), \
                      (65/6., r_bound), (75/6., l_bound), (85/6., r_bound), \
                      (95/6., l_bound), (105/6., r_bound), (115/6., l_bound)]

        tacks = [cartesian_to_polar(x, y) for (x, y) in tacks_cart]
        tacks = [(rng, bearing + waypoint[1]) for (rng, bearing) in tacks]

        np.testing.assert_almost_equal(tacks,  place_tacks(waypoint, mock_boat, mock_wind, config))
