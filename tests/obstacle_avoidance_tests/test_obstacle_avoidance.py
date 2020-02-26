import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from pubsub import pub
from time import sleep
import numpy as np

from src.autonomy.obstacle_avoidance.obstacle_avoidance import ObstacleAvoidance, mutex_waypoint, mutex_object_field

class ObstacleAvoidanceTests(unittest.TestCase):
    """Tests methods in Obstacle Avoidance class"""
    def setUp(self):
        """Initializes obstacle avoidance class"""
        # ensure obstacle avoidance mutexes are released
        if mutex_waypoint.locked():
            mutex_waypoint.release()
        if mutex_object_field.locked():
            mutex_object_field.release()

        self.obstacle_avoidance = ObstacleAvoidance(None, None)

    @patch('src.autonomy.obstacle_avoidance.obstacle_avoidance.ObstacleAvoidance.get_objects')
    @patch('src.autonomy.obstacle_avoidance.obstacle_avoidance.ObstacleAvoidance.find_path')
    @patch('src.autonomy.obstacle_avoidance.obstacle_avoidance.sleep')
    @patch('src.autonomy.obstacle_avoidance.obstacle_avoidance.pub.sendMessage')
    def test_run(self, mock_pub, mock_sleep, mock_find_path, mock_get_objects):
        """Tests run method of obstacle avoidance"""
        adjusted_heading = 1
        mock_find_path.return_value = adjusted_heading

        # start run thread
        self.obstacle_avoidance.start()

        # check that methods are called (and with correct args)
        mock_get_objects.assert_any_call()
        mock_find_path.assert_any_call()
        mock_pub.assert_called_with('set heading', heading = adjusted_heading)
        mock_sleep.assert_called_with(self.obstacle_avoidance.update_interval)

        self.obstacle_avoidance.is_active = False

    def test_update_waypoint(self):
        """Tests update waypoint method of obstacle avoidance"""
        # generate test waypoints
        waypoints = [(1, 1), (10, -50), (22.532, 123.321)]

        # loop through values
        for waypoint in waypoints:
            # publish to waypoint channel
            pub.sendMessage('waypoint', new_waypoint=waypoint)

            # check for correct behavior
            self.assertTupleEqual(waypoint, self.obstacle_avoidance.waypoint)

    def test_quit(self):
        """Tests quit method of obstacle avoidance"""
        # ensure starting state is true
        self.assertEqual(True, self.obstacle_avoidance.is_active)

        # call quit method
        self.obstacle_avoidance.quit()

        # ensure state is false
        self.assertEqual(False, self.obstacle_avoidance.is_active)

    def test_get_objects(self):
        """Tests get objects method of obstacle avoidance"""
        # set time and bearing range
        time_range = (0, 3000)
        bearing_range = (-25, 25)
        self.obstacle_avoidance.object_field_config = {'time_range': time_range, 'bearing_range': bearing_range,
                                                       'num_predictions': False}

        # mock return val for tracker return_objects method
        truth_object_field = [(1, 2, 0, 0, 0), (2, 3, 1, 0, 0)]
        mock_tracker = MagicMock(name='Map')
        self.obstacle_avoidance.tracker = mock_tracker
        mock_tracker.return_objects.return_value = truth_object_field

        # call get objects method
        self.obstacle_avoidance.get_objects()

        # check that return objects was called with correct args
        mock_tracker.return_objects.assert_called_with(bearingRange = bearing_range, timeRange = time_range)

        # check that object field was set to correct value
        self.assertListEqual(truth_object_field, self.obstacle_avoidance.object_field)

    @patch('src.autonomy.obstacle_avoidance.obstacle_avoidance.ObstacleAvoidance.create_gap_matrix')
    def test_find_path(self, mock_gap_mat):
        """Tests find path method of obstacle avoidance"""
        # --------------------------------------------------------
        # Testing methodology:
        #   - 3 tests (no adjust needed (no obstacles), no adjust needed (some obstacles), adjust needed)
        #   - check returned matrix vs hand-created comparison
        # --------------------------------------------------------
        self.obstacle_avoidance.object_field = []
        
        # -------- Test 1 (No obstacles, no adjust needed) ---------------------------
        # create gap matrix
        gap_matrix = np.ones((5, 5))        # create 5x5 gap matrix (no obstacles)
        theta_list = [*range(-2, 3)]

        # set up mock create gap matrix
        mock_gap_mat.return_value = gap_matrix, theta_list

        # set up waypoint
        desired_heading = 1
        self.obstacle_avoidance.waypoint = (10, desired_heading)

        # no change to heading
        truth_adjusted_heading = desired_heading

        # check for correct behavior
        self.assertEqual(self.obstacle_avoidance.find_path(), truth_adjusted_heading)

        # -------- Test 2 (Obstacles, no adjust needed) ---------------------------
        self.obstacle_avoidance.object_field = [0]
        # create gap matrix
        gap_matrix = np.ones((5, 5))        # create 5x5 gap matrix (no obstacles)
        gap_matrix[3, 0] = 0
        gap_matrix[4, 2] = 0
        theta_list = [*range(-2, 3)]

        # set up mock create gap matrix
        mock_gap_mat.return_value = gap_matrix, theta_list

        # set up waypoint
        desired_heading = -1
        self.obstacle_avoidance.waypoint = (10, desired_heading)

        # no change to heading
        truth_adjusted_heading = desired_heading

        # check for correct behavior
        self.assertEqual(truth_adjusted_heading, self.obstacle_avoidance.find_path())

        # -------- Test 3 (Obstacles, adjust needed) ---------------------------
        # create gap matrix
        gap_matrix = np.ones((5, 5))        # create 5x5 gap matrix (no obstacles)
        gap_matrix[2, 0] = 0
        gap_matrix[3, 1] = 0
        theta_list = [*range(-2, 3)]

        # set up mock create gap matrix
        mock_gap_mat.return_value = gap_matrix, theta_list

        # set up waypoint
        desired_heading = -1
        self.obstacle_avoidance.waypoint = (10, desired_heading)

        # no change to heading
        truth_adjusted_heading = 0

        # check for correct behavior
        self.assertEqual(self.obstacle_avoidance.find_path(), truth_adjusted_heading)

    def test_create_gap_matrix(self):
        """Tests create gap matrix method of obstacle avoidance"""
        # --------------------------------------------------------
        # Testing methodology:
        #   - 4 tests (no overlap, 50% overlap, 75% overlap, 50% overlap AND predictions)
        #   - check returned matrix vs hand-created comparison
        # --------------------------------------------------------

        # -------- Test 1 (0% overlap) ---------------------------

        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}
        # create bounds
        self.obstacle_avoidance.t_bounds = [(x/2, (x+1)/2) for x in range(10)]
        self.obstacle_avoidance.theta_bounds = [(x, x+1) for x in range(-25, 25)]

        # set boat speed
        boat_speed = 1
        mock_boat = MagicMock(name='boat')
        self.obstacle_avoidance.boat = mock_boat
        mock_boat.current_speed.return_value = boat_speed

        # initialize truth gap matrix
        truth_gap_matrix = np.ones((10, 50))

        # set object field -- 5 objects (2 in same field, 3 in different fields)
        object_field = [0] * 5
        object_field[0] = (0.75, 20.5, 0, 0, 0)
        truth_gap_matrix[1, 45] = 0
        object_field[1] = (0.85, 20.75, 0, 0, 0)    # in same field as prev object
        object_field[2] = (4.2, 1.1, 0, 0, 0)
        truth_gap_matrix[8, 26] = 0
        object_field[3] = (4.2, -1.1, 0, 0, 0)
        truth_gap_matrix[8, 23] = 0
        object_field[4] = (3.89, -5.0, 0, 0, 0)
        truth_gap_matrix[7, 19] = 0
        truth_gap_matrix[7, 20] = 0
       
        self.obstacle_avoidance.object_field = object_field 

        # generate truth theta list
        truth_theta_list = [val+0.5 for val in range(-25, 25)]

        # check for correct behavior
        gap_mat, theta_list = self.obstacle_avoidance.create_gap_matrix()
        np.testing.assert_array_equal(truth_gap_matrix, gap_mat)
        self.assertListEqual(truth_theta_list, theta_list)

        # -------- Test 2 (50% overlap) ---------------------------

        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.5}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}
        # create bounds
        self.obstacle_avoidance.t_bounds = [(x/4, (x/4)+(1/2)) for x in range(19)] + [(4.75, 5)]
        self.obstacle_avoidance.theta_bounds = [(x/2, (x/2)+1) for x in range(-50, 49)] + [(24.5, 25)]

        # set boat speed
        boat_speed = 1
        mock_boat = MagicMock(name='boat')
        self.obstacle_avoidance.boat = mock_boat
        mock_boat.current_speed.return_value = boat_speed

        # initialize truth gap matrix
        truth_gap_matrix = np.ones((20, 100))

        # set object field -- 5 objects
        object_field = [0] * 5
        object_field[0] = (0.75, 20.5, 0, 0, 0)
        truth_gap_matrix[1, 89] = 0
        truth_gap_matrix[2, 89] = 0
        truth_gap_matrix[3, 89] = 0
        truth_gap_matrix[1, 90] = 0
        truth_gap_matrix[2, 90] = 0
        truth_gap_matrix[3, 90] = 0
        truth_gap_matrix[1, 91] = 0
        truth_gap_matrix[2, 91] = 0
        truth_gap_matrix[3, 91] = 0
        object_field[1] = (0.85, 20.75, 0, 0, 0)    # in same field as prev object
        object_field[2] = (4.2, 1.1, 0, 0, 0)
        truth_gap_matrix[15, 51] = 0
        truth_gap_matrix[16, 51] = 0
        truth_gap_matrix[15, 52] = 0
        truth_gap_matrix[16, 52] = 0
        object_field[3] = (4.2, -1.1, 0, 0, 0)
        truth_gap_matrix[15, 46] = 0
        truth_gap_matrix[16, 46] = 0
        truth_gap_matrix[15, 47] = 0
        truth_gap_matrix[16, 47] = 0
        object_field[4] = (3.89, -5.0, 0, 0, 0)
        truth_gap_matrix[14, 38] = 0
        truth_gap_matrix[15, 38] = 0
        truth_gap_matrix[14, 39] = 0
        truth_gap_matrix[15, 39] = 0
        truth_gap_matrix[14, 40] = 0
        truth_gap_matrix[15, 40] = 0
       
        self.obstacle_avoidance.object_field = object_field 

        # generate truth theta list
        truth_theta_list = [((val/2)+0.5) for val in range(-50, 49)] + [24.75]

        # check for correct behavior
        gap_mat, theta_list = self.obstacle_avoidance.create_gap_matrix()
        np.testing.assert_array_equal(truth_gap_matrix, gap_mat)
        self.assertListEqual(truth_theta_list, theta_list)

        # -------- Test 3 (75% overlap) ---------------------------

        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.75}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}
        # create bounds
        self.obstacle_avoidance.t_bounds = [(x/8, (x/8)+(1/2)) for x in range(37)] + [(4.625, 5), (4.75, 5), (4.875, 5)]
        self.obstacle_avoidance.theta_bounds = [(x/4, (x/4)+1) for x in range(-100, 97)] + [(24.25, 25), (24.5, 25), (24.75, 25)]

        # set boat speed
        boat_speed = 1
        mock_boat = MagicMock(name='boat')
        self.obstacle_avoidance.boat = mock_boat
        mock_boat.current_speed.return_value = boat_speed

        # initialize truth gap matrix
        truth_gap_matrix = np.ones((40, 200))

        # set object field -- 5 objects
        object_field = [0] * 5
        object_field[0] = (0.75, 20.5, 0, 0, 0)
        truth_gap_matrix[2, 178] = 0
        truth_gap_matrix[3, 178] = 0
        truth_gap_matrix[4, 178] = 0
        truth_gap_matrix[5, 178] = 0
        truth_gap_matrix[6, 178] = 0
        truth_gap_matrix[2, 179] = 0
        truth_gap_matrix[3, 179] = 0
        truth_gap_matrix[4, 179] = 0
        truth_gap_matrix[5, 179] = 0
        truth_gap_matrix[6, 179] = 0
        truth_gap_matrix[2, 180] = 0
        truth_gap_matrix[3, 180] = 0
        truth_gap_matrix[4, 180] = 0
        truth_gap_matrix[5, 180] = 0
        truth_gap_matrix[6, 180] = 0
        truth_gap_matrix[2, 181] = 0
        truth_gap_matrix[3, 181] = 0
        truth_gap_matrix[4, 181] = 0
        truth_gap_matrix[5, 181] = 0
        truth_gap_matrix[6, 181] = 0
        truth_gap_matrix[2, 182] = 0
        truth_gap_matrix[3, 182] = 0
        truth_gap_matrix[4, 182] = 0
        truth_gap_matrix[5, 182] = 0
        truth_gap_matrix[6, 182] = 0
        object_field[1] = (0.85, 20.75, 0, 0, 0)    # in same field as prev object
        truth_gap_matrix[3, 179] = 0
        truth_gap_matrix[4, 180] = 0
        truth_gap_matrix[5, 181] = 0
        truth_gap_matrix[6, 182] = 0
        truth_gap_matrix[3, 183] = 0
        truth_gap_matrix[4, 183] = 0
        truth_gap_matrix[5, 183] = 0
        truth_gap_matrix[6, 183] = 0
        object_field[2] = (4.2, 1.1, 0, 0, 0)
        truth_gap_matrix[30, 101] = 0
        truth_gap_matrix[31, 101] = 0
        truth_gap_matrix[32, 101] = 0
        truth_gap_matrix[33, 101] = 0
        truth_gap_matrix[30, 102] = 0
        truth_gap_matrix[31, 102] = 0
        truth_gap_matrix[32, 102] = 0
        truth_gap_matrix[33, 102] = 0
        truth_gap_matrix[30, 103] = 0
        truth_gap_matrix[31, 103] = 0
        truth_gap_matrix[32, 103] = 0
        truth_gap_matrix[33, 103] = 0
        truth_gap_matrix[30, 104] = 0
        truth_gap_matrix[31, 104] = 0
        truth_gap_matrix[32, 104] = 0
        truth_gap_matrix[33, 104] = 0
        object_field[3] = (4.2, -1.1, 0, 0, 0)
        truth_gap_matrix[30, 92] = 0
        truth_gap_matrix[31, 92] = 0
        truth_gap_matrix[32, 92] = 0
        truth_gap_matrix[33, 92] = 0
        truth_gap_matrix[30, 93] = 0
        truth_gap_matrix[31, 93] = 0
        truth_gap_matrix[32, 93] = 0
        truth_gap_matrix[33, 93] = 0
        truth_gap_matrix[30, 94] = 0
        truth_gap_matrix[31, 94] = 0
        truth_gap_matrix[32, 94] = 0
        truth_gap_matrix[33, 94] = 0
        truth_gap_matrix[30, 95] = 0
        truth_gap_matrix[31, 95] = 0
        truth_gap_matrix[32, 95] = 0
        truth_gap_matrix[33, 95] = 0
        object_field[4] = (3.89, -5.0, 0, 0, 0)
        truth_gap_matrix[28, 76] = 0
        truth_gap_matrix[29, 76] = 0
        truth_gap_matrix[30, 76] = 0
        truth_gap_matrix[31, 76] = 0
        truth_gap_matrix[28, 77] = 0
        truth_gap_matrix[29, 77] = 0
        truth_gap_matrix[30, 77] = 0
        truth_gap_matrix[31, 77] = 0
        truth_gap_matrix[28, 78] = 0
        truth_gap_matrix[29, 78] = 0
        truth_gap_matrix[30, 78] = 0
        truth_gap_matrix[31, 78] = 0
        truth_gap_matrix[28, 79] = 0
        truth_gap_matrix[29, 79] = 0
        truth_gap_matrix[30, 79] = 0
        truth_gap_matrix[31, 79] = 0
        truth_gap_matrix[28, 80] = 0
        truth_gap_matrix[29, 80] = 0
        truth_gap_matrix[30, 80] = 0
        truth_gap_matrix[31, 80] = 0
       
        self.obstacle_avoidance.object_field = object_field 

        # generate truth theta list
        truth_theta_list = [((val/4)+0.5) for val in range(-100, 97)] + [24.625, 24.75, 24.875]

        # check for correct behavior
        gap_mat, theta_list = self.obstacle_avoidance.create_gap_matrix()
        np.testing.assert_array_equal(truth_gap_matrix, gap_mat)
        self.assertListEqual(truth_theta_list, theta_list)

        # -------- Test 4 (50% overlap AND predictions) ---------------------------

        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.5}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 5}
        # create bounds
        self.obstacle_avoidance.t_bounds = [(x/4, (x/4)+(1/2)) for x in range(19)] + [(4.75, 5)]
        self.obstacle_avoidance.theta_bounds = [(x/2, (x/2)+1) for x in range(-50, 49)] + [(24.5, 25)]

        # set boat speed
        boat_speed = 1
        mock_boat = MagicMock(name='boat')
        self.obstacle_avoidance.boat = mock_boat
        mock_boat.current_speed.return_value = boat_speed

        # initialize truth gap matrix
        truth_gap_matrix = np.ones((20, 100))

        # set object field -- 5 objects
        object_field = [0] * 5
        object_field[0] = (0.75, 20.5, 0, 0, 0.25)         # bearing movement
        truth_gap_matrix[1, 89] = 0
        truth_gap_matrix[2, 89] = 0
        truth_gap_matrix[3, 89] = 0
        truth_gap_matrix[1, 90] = 0
        truth_gap_matrix[2, 90] = 0
        truth_gap_matrix[3, 90] = 0
        truth_gap_matrix[1, 91] = 0
        truth_gap_matrix[2, 91] = 0
        truth_gap_matrix[3, 91] = 0
        truth_gap_matrix[1, 92] = 0
        truth_gap_matrix[2, 92] = 0
        truth_gap_matrix[3, 92] = 0
        object_field[1] = (0.85, 20.75, 0, 0, 0)    # in overlapping fields w prev object
        object_field[2] = (4.2, 1.1, 0, 0.2, 0)
        truth_gap_matrix[15, 51] = 0
        truth_gap_matrix[16, 51] = 0
        truth_gap_matrix[17, 51] = 0
        truth_gap_matrix[18, 51] = 0
        truth_gap_matrix[15, 52] = 0
        truth_gap_matrix[16, 52] = 0
        truth_gap_matrix[17, 52] = 0
        truth_gap_matrix[18, 52] = 0
        object_field[3] = (4.2, -1.1, 0, 0.18, -0.5)
        truth_gap_matrix[15, 47] = 0
        truth_gap_matrix[15, 46] = 0
        truth_gap_matrix[16, 47] = 0
        truth_gap_matrix[16, 46] = 0
        truth_gap_matrix[16, 45] = 0
        truth_gap_matrix[17, 47] = 0
        truth_gap_matrix[17, 46] = 0
        truth_gap_matrix[17, 45] = 0
        truth_gap_matrix[17, 44] = 0
        truth_gap_matrix[18, 45] = 0
        truth_gap_matrix[18, 44] = 0
        object_field[4] = (3.89, -5.0, 0, 0, 0)
        truth_gap_matrix[14, 38] = 0
        truth_gap_matrix[15, 38] = 0
        truth_gap_matrix[14, 39] = 0
        truth_gap_matrix[15, 39] = 0
        truth_gap_matrix[14, 40] = 0
        truth_gap_matrix[15, 40] = 0
       
        self.obstacle_avoidance.object_field = object_field 

        # generate truth theta list
        truth_theta_list = [((val/2)+0.5) for val in range(-50, 49)] + [24.75]

        # check for correct behavior
        gap_mat, theta_list = self.obstacle_avoidance.create_gap_matrix()
        np.testing.assert_array_equal(truth_gap_matrix, gap_mat)
        self.assertListEqual(truth_theta_list, theta_list)

    def test_make_time_bounds(self):
        """Tests make time bounds method"""
        # -------- Test 1 (0% overlap) ---------------------------
        # set overlap, steps, and ranges
        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}

        # generate truth time bounds
        truth_t_bounds = [(x/2, (x+1)/2) for x in range(10)]

        # call make time bounds
        self.obstacle_avoidance._make_time_bounds()

        # check for correct behavior
        self.assertListEqual(truth_t_bounds, self.obstacle_avoidance.t_bounds)

        # -------- Test 2 (50% overlap) ---------------------------
        # set overlap, steps, and ranges
        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.5}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}

        # generate truth time bounds
        truth_t_bounds = [(x/4, (x/4)+(1/2)) for x in range(19)] + [(4.75, 5)]

        # call make time bounds
        self.obstacle_avoidance._make_time_bounds()

        # check for correct behavior
        self.assertListEqual(truth_t_bounds, self.obstacle_avoidance.t_bounds)

        # -------- Test 3 (75% overlap) ---------------------------
        # set overlap, steps, and ranges
        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.75}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}

        # generate truth time bounds
        truth_t_bounds = [(x/8, (x/8)+(1/2)) for x in range(37)] + [(4.625, 5), (4.75, 5), (4.875, 5)]

        # call make time bounds
        self.obstacle_avoidance._make_time_bounds()

        # check for correct behavior
        self.assertListEqual(truth_t_bounds, self.obstacle_avoidance.t_bounds)

    def test_make_theta_bounds(self):
        """Tests make theta bounds method"""
        # -------- Test 1 (0% overlap) ---------------------------
        # set overlap, steps, and ranges
        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}

        # generate truth theta bounds
        truth_theta_bounds = [(x, x+1) for x in range(-25, 25)]

        # call make theta bounds
        self.obstacle_avoidance._make_theta_bounds()

        # check for correct behavior
        self.assertListEqual(truth_theta_bounds, self.obstacle_avoidance.theta_bounds)

        # -------- Test 2 (50% overlap) ---------------------------
        # set overlap, steps, and ranges
        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.5}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}

        # generate truth theta bounds
        truth_theta_bounds = [(x/2, (x/2)+1) for x in range(-50, 49)] + [(24.5, 25)]

        # call make time bounds
        self.obstacle_avoidance._make_theta_bounds()

        # check for correct behavior
        self.assertListEqual(truth_theta_bounds, self.obstacle_avoidance.theta_bounds)

        # -------- Test 3 (75% overlap) ---------------------------
        # set overlap, steps, and ranges
        self.obstacle_avoidance.gap_config = {'t_step':  0.5, 'theta_step': 1, 'overlap': 0.75}
        self.obstacle_avoidance.object_field_config = {'time_range': (0, 5), 'bearing_range': (-25, 25),
                                                       'num_predictions': 0}

        # generate truth theta bounds
        truth_theta_bounds = [(x/4, (x/4)+1) for x in range(-100, 97)] + [(24.25, 25), (24.5, 25), (24.75, 25)]

        # call make theta bounds
        self.obstacle_avoidance._make_theta_bounds()

        # check for correct behavior
        self.assertListEqual(truth_theta_bounds, self.obstacle_avoidance.theta_bounds)
