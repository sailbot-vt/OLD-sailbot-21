import unittest
import math

from src.world.wind import Wind

class WindTests(unittest.TestCase):
    """Tests the methods in Wind"""
    def setUp(self):
        self.wind = Wind()

    def test_angle_relative_to_true_wind(self):
        """Tests that the conversion to angle relative to wind works"""
        test_inputs = [(15, 30), (15, 0), (37, 37), (186, 8), (275, 300)]
        scaled_outputs = [15, -15, 0, -178, 25]

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            self.wind.true_wind_angle = test_input[1]
            self.assertAlmostEqual(scaled_output, self.wind.angle_relative_to_wind(test_input[0]))

    def test_distance_upwind(self):
        """Tests that we measure distance upwind correctly"""
        test_inputs = [
            ((0, 0), (1, 0), 0),
            ((1, 0), (0, 0), 0),
            ((1, 0), (0, 0), 135),
            ((1, 180), (0, 0), 135)
        ]
        scaled_outputs = [1, -1, 1 / math.sqrt(2), -1 / math.sqrt(2), 0]

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            self.wind.true_wind_angle = test_input[2]
            self.assertAlmostEqual(scaled_output, self.wind.distance_upwind(test_input[0], test_input[1]), places=3)


if __name__ == "__main__":
    unittest.main()
