import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

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
        pass

    def test_quit(self):
        """Tests quit method of obstacle avoidance"""
        pass

    def test_get_objects(self):
        """Tests get objects method of obstacle avoidance"""
        pass

    def test_find_path(self):
        """Tests find path method of obstacle avoidance"""
        pass

    def test_create_gap_matrix(self):
        """Tests create gap matrix method of obstacle avoidance"""
        pass
