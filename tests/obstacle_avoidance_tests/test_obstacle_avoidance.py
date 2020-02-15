import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from pubsub import pub

from src.autonomy.obstacle_avoidance.obstacle_avoidance import ObstacleAvoidance

class ObstacleAvoidanceTests(unittest.TestCase):
    """Tests methods in Obstacle Avoidance class"""
    def setUp(self):
        """Initializes obstacle avoidance class"""
        self.obstacle_avoidance = ObstacleAvoidance(None, None, None)

    def test_run(self):
        """Tests run method of obstacle avoidance"""
        pass

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
        self.obstacle_avoidance.object_field_config = {'time_range': time_range, 'bearing_range': bearing_range}

        # mock return val for tracker return_objects method
        truth_object_field = [(1, 2, 0), (2, 3, 1)]
        mock_tracker = MagicMock(name='Map')
        self.obstacle_avoidance.tracker = mock_tracker
        mock_tracker.return_objects.return_value = truth_object_field

        # call get objects method
        self.obstacle_avoidance.get_objects()

        # check that return objects was called with correct args
        mock_tracker.return_objects.assert_called_with(bearingRange = bearing_range, timeRange = time_range)

        # check that object field was set to correct value
        self.assertListEqual(truth_object_field, self.obstacle_avoidance.object_field)

    def test_find_path(self):
        """Tests find path method of obstacle avoidance"""
        pass

    def test_create_gap_matrix(self):
        """Tests create gap matrix method of obstacle avoidance"""
        pass
