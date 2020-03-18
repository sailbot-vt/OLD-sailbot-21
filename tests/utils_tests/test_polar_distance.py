import unittest

import numpy as np

from src.utils.coord_conv import cartesian_to_polar

from src.utils.polar_distance import polar_distance

class PolarDistanceTests(unittest.TestCase):
    """Tests Polar distance"""
    def setUp(self):
        pass

    def test_polar_distance(self):
        """Tests polar distance method"""
        # generate test pairs
        test_pairs_cart = [[(5, 2.5), (5, -2.5)],
                           [(5, 2.5), (10, 2.5)],
                           [(5, 12.5), (5, 7.5)],
                           [(10, 10), (20, 0)],
                           [(80, 57), (82.5, 59.5)]]

        test_pairs = [[cartesian_to_polar(x, y) for x, y in coord_pair] for coord_pair in test_pairs_cart]

        # generate truth distances
        truth_dists = [5, 5, 5, np.sqrt(200), 3.535533906]

        # check for correct behavior
        for pair, dist in zip(test_pairs, truth_dists):
            self.assertAlmostEqual(dist, polar_distance(pair))
