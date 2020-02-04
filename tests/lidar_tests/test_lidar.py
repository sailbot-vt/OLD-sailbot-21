import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from time import sleep

from statistics import median
from src.lidar.lidar import LiDAR

#TODO REMOVE
import pdb

class LiDARTests(unittest.TestCase):
    """Tests the methods in LiDAR"""
    def setUp(self):
        boat = MagicMock()
        self.sensor_val = 10
        boat.get_current_sensor_value.return_value = self.sensor_val
        self.lidar = LiDAR(boat)

    def test_store_rng(self):
        """Tests store rng method of LiDAR"""
        # generate input and truth vals
        vals = [1, 2, 3, 4, 5, 6]
        truth_raw_data = [[1, 0, 0, 0, 0],
                          [2, 1, 0, 0, 0],
                          [3, 2, 1, 0, 0],
                          [4, 3, 2, 1, 0],
                          [5, 4, 3, 2, 1],
                          [6, 5, 4, 3, 2]]

        # loop through vals and check for correct behavior
        for val, truth_raw in zip(vals, truth_raw_data):
            self.lidar.store_rng(val)

            self.assertEqual(truth_raw, self.lidar.raw_data)

    @patch('src.lidar.lidar.pub', autospec=True)
    def test_publish(self, mock_pub):
        """Tests publish method of LiDAR"""
        # build raw data lists
        raw_data_lists = [[-1, -1, -1, -1, -1],             # all bad data
                          [-1, 10, -1, 11, -1],             # majority bad data
                          [-1, 16, 16.15, 15.75, -1],       # mostly good data, not within error margin (0.1 m)
                          [52.0, 52.09, 51.98, -1, 51.95],  # mostly good data, within error margin (should publish)
                          [109.11, 109.09, 109.15, 109.12, 109.12]]  # all good data, within error margin (should publish)

        outputs = [None, None, None, median(raw_data_lists[3]), median(raw_data_lists[4])]

        # run publish for each data list
        for data_list, output in zip(raw_data_lists, outputs):
            # set data list
            self.lidar.raw_data = data_list

            # call publish
            self.lidar.publish()

            # check that pub message was sent correctly (or not sent)
            if output is None:
                mock_pub.sendMessage.assert_not_called()
            else:
                mock_pub.sendMessage.assert_called_with('LiDAR data', bearing=self.sensor_val, rng=output)

            # reset mock
            mock_pub.reset_mock()

    def test_exit(self):
        """Tests exit method of LiDAR"""
        # set starting state to False
        self.lidar.keep_reading = True

        # ensure starting state is True
        self.assertEqual(True, self.lidar.keep_reading)

        # call exit 
        self.lidar.exit()

        # assert correct behavior
        self.assertEqual(False, self.lidar.keep_reading)

    @patch('src.lidar.lidar.LiDAR.publish')
    @patch('src.lidar.lidar.sleep')
    def test_run(self, mock_sleep, mock_publish):
        """Tests run method of LiDAR"""
        # start LiDAR thread
        self.lidar.start()

        # sleep to ensure that methods get called
        sleep(0.05)

        # check that publish is being called
        self.assertEqual(True, mock_publish.called)

        # check that sleep is being called with publish interval
        mock_sleep.assert_called_with(self.lidar.publish_interval)

        # stop lidar thread
        self.lidar.keep_reading = False
        sleep(0.05)                         # gives time for loop to exit

        # reset mocks
        mock_sleep.reset_mock()
        mock_publish.reset_mock()

        # sleep to give time for methods to (not) be called
        sleep(0.05)

        # check that methods are NOT called
        self.assertEqual(False, mock_sleep.called)
        self.assertEqual(False, mock_publish.called)

if __name__ == "__main__":
    unittest.main()
