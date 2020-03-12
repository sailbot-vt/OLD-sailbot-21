import os
import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from src.autonomy.movement.movement import Movement 

class MovementTests(unittest.TestCase):
    """Tests methods in Movement Thread"""
    def setUp(self):
        """Sets up movement class"""
        # set up mock wind
        self.wind = MagicMock(name = "Wind")

        self.movement = Movement(self.wind)

    def tearDown(self):
        """Cleans up movement thread"""
        self.movement.is_active = False

    @patch('src.autonomy.movement.movement.Movement.set_sail')
    @patch('src.autonomy.movement.movement.Movement.set_jib')
    @patch('src.autonomy.movement.movement.sleep')
    def test_run(self, mock_sleep, mock_set_jib, mock_set_sail):
        """Tests run method of movement thread"""
        # start thread
        self.movement.start()

        # check that set sail, set jib, and sleep are called
        mock_set_sail.assert_any_call()
        mock_set_jib.assert_any_call()
        mock_sleep.assert_any_call(self.movement.update_interval)

        # stop thread
        self.movement.is_active = False

        # reset mocks
        mock_set_sail.reset_mock()
        mock_set_jib.reset_mock()
        mock_sleep.reset_mock()

        # check that set sail, set jib, and sleep are NOT called
        mock_set_sail.assert_not_called()
        mock_set_jib.assert_not_called()
        mock_sleep.assert_not_called()

    def test_quit(self):
        """Tests quit method of movement thread"""
        # set to active
        self.movement.is_active = True

        # call quit method
        self.movement.quit()

        # check for correct behavior
        self.assertEqual(False, self.movement.is_active)

    @patch('src.autonomy.movement.movement.Movement.set_rudder')
    def test_set_heading(self, mock_set_rudder):
        """Tests set heading method of movement thread"""
        # call set heading with arbitrary heading
        truth_heading = 30
        self.movement.set_heading(truth_heading)

        # check for correct behavior
        mock_set_rudder.assert_called_with(truth_heading)

    @patch('src.autonomy.movement.movement.pub.sendMessage')
    def test_set_rudder(self, mock_send_msg):
        """Tests set rudder method of movement thread"""
        # set rudder angle
        self.rudder_angle = 10

        # check for correct behavior
        self.movement.set_rudder(1)     # positive angle
        mock_send_msg.assert_called_with("set rudder", self.rudder_angle)

        mock_send_msg.reset_mock()
        self.movement.set_rudder(-1)     # negative angle
        mock_send_msg.assert_called_with("set rudder", -1 * self.rudder_angle)

    def test_set_sail(self):
        """Tests set sail method of movement thread"""
        pass

    def test_set_jib(self):
        """Tests set jib method of movement thread"""
        pass
