import unittest

from src.world.wind import Wind


class WindTests(unittest.TestCase):
    """Tests the methods in rudder"""

    def test_angle_relative_to_true_wind(self):
        test_inputs = [(15, 30), (15, 0), (37, 37), (186, 8), (275, 300)]
        scaled_outputs = [15, -15, 0, -178, 25]

        w = Wind()

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            w.true_wind_angle = test_input[1]
            self.assertAlmostEqual(scaled_output, w.angle_relative_to_wind(test_input[0]))


if __name__ == "__main__":
    unittest.main()
