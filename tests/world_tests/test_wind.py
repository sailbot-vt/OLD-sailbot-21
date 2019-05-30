import unittest
import math

from src.world.wind import Wind
from src.gps_point import GPSPoint


class WindTests(unittest.TestCase):
    """Tests the methods in Wind"""

    def test_angle_relative_to_true_wind(self):
        """Tests that the conversion to angle relative to wind works"""
        test_inputs = [(15, 30), (15, 0), (37, 37), (186, 8), (275, 300)]
        scaled_outputs = [15, -15, 0, -178, 25]

        w = Wind()

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            w.true_wind_angle = test_input[1]
            self.assertAlmostEqual(scaled_output, w.angle_relative_to_wind(test_input[0]))

    def test_distance_upwind(self):
        """Tests that we measure distance upwind correctly"""
        test_inputs = [
            ((0, 0), (1, 0), 0),
            ((1, 0), (0, 0), 0),
            ((1, 0), (0, 0), 135),
            ((-1, 0), (0, 0), 135)
        ]
        scaled_outputs = [1, -1, 1 / math.sqrt(2), -1 / math.sqrt(2), 0]

        w = Wind()

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            a = GPSPoint(test_input[0][0], test_input[0][1])
            b = GPSPoint(test_input[1][0], test_input[1][1])
            w.true_wind_angle = test_input[2]
            self.assertAlmostEqual(scaled_output, w.distance_upwind(a, b))


if __name__ == "__main__":
    unittest.main()
