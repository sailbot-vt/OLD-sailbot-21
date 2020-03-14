import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import numpy as np
from statistics import mean

from src.utils.coord_conv import cartesian_to_polar

from src.autonomy.feature_extraction.find_start_gate import find_start_gate, _find_centerpoint, _polar_distance

class FindStartGateTests(unittest.TestCase):
    """Tests the methods in find start gate"""
    def setUp(self):
        pass

    @patch('src.autonomy.feature_extraction.find_start_gate._find_centerpoint', return_value = None)
    def test_find_start_gate(self, mock_centerpoint):
        """Tests find start gate method"""
        config = {'width': 5, 'width_variance': 1.5}
        # generate test buoy arrays
        test_buoys_cart = [((5, 2.5), (5, -2.5)),                       # just gate in array 
                           ((5, 2.5), (42, -18), (10, 2.5)),            # gate + extra buoy
                           ((5, 12.5), (5, 7.5), (89, 22), (12, 80)),   # gate + extra buoys
                           ((80, 57), (82.7, 59.5), (5, 2.5), (5, -2.4)),   # two possible gates (one pair with lower confidence than other)
                           ((20, 50), (58, 75)),            # no possible gates
                           ()]                               # empty list

        test_buoys = [tuple(cartesian_to_polar(x, y) for x, y in coord_pair) for coord_pair in test_buoys_cart]

        truth_gates_cart = [((5, 2.5), (5, -2.5)),
                            ((5, 2.5), (10, 2.5)),
                            ((5, 12.5), (5, 7.5)),
                            ((5, 2.5), (5, -2.4)),
                            None,
                            None]

        truth_gates = [tuple(cartesian_to_polar(x, y) for x, y in coord_pair) if coord_pair is not None \
                                                                              else None for coord_pair in truth_gates_cart]

        # check for correct behavior
        for truth_gate, test_buoy_set in zip(truth_gates, test_buoys):
            _, return_gate = find_start_gate(test_buoy_set, config)
            if return_gate is not None:
                np.testing.assert_almost_equal(truth_gate, return_gate)
            else:
                self.assertIsNone(truth_gate)
        
    def test_find_centerpoint(self):
        """Tests find centerpoint method"""
        # generate test gates
        test_buoys_cart = [((5, 2.5), (5, -2.5)),
                           ((5, 2.5), (10, 2.5)),
                           ((5, 12.5), (5, 7.5)),
                           ((80, 57), (82.5, 59.5))]

        test_buoys = [tuple(cartesian_to_polar(x, y) for x, y in coord_pair) for coord_pair in test_buoys_cart]

        # calculate centerpoints
        test_centerpoints_cart = [(mean((x1, x2)), mean((y1, y2))) for (x1, y1), (x2, y2) in test_buoys_cart]
        truth_centerpoints = [cartesian_to_polar(x, y) for (x, y) in test_centerpoints_cart]

        # check for correct behavior
        for gate, truth_center in zip(test_buoys, truth_centerpoints):
            np.testing.assert_almost_equal(truth_center, _find_centerpoint(gate))

    def test_polar_distance(self):
        """Tests polar distance method"""
        # generate test pairs
        test_pairs_cart = [[(5, 2.5), (5, -2.5)],
                           [(5, 2.5), (10, 2.5)],
                           [(5, 12.5), (5, 7.5)],
                           [(80, 57), (82.5, 59.5)]]

        test_pairs = [[cartesian_to_polar(x, y) for x, y in coord_pair] for coord_pair in test_pairs_cart]

        # generate truth distances
        truth_dists = [5, 5, 5, 3.535533906]

        # check for correct behavior
        for pair, dist in zip(test_pairs, truth_dists):
            self.assertAlmostEqual(dist, _polar_distance(pair))
