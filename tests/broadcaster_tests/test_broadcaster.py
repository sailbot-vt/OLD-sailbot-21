import os
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from src.broadcaster.broadcaster import BroadcasterType, make_broadcaster


class BroadcasterTests(unittest.TestCase):
    """ Tests Broadcaster methods. """

    def setUp(self):
        """ Create testing fields """
        self.path = os.path.dirname(os.path.abspath(__file__))
        try:
            os.remove(self.path + "/broadcast_test.log")
        except:
            pass
        self.testable = make_broadcaster()
        self.messenger = make_broadcaster(
            broadcaster_type=BroadcasterType.Messenger)
        self.filewriter = make_broadcaster(
            broadcaster_type=BroadcasterType.FileWriter, 
            filename=self.path + "/broadcast_test.log")
        self.data = {
            1 : "test",
            2 : "test2",
            3 : "test3"
        }

    def test_update_data(self):
        """ Tests update data for broadcasters """
        self.assertEqual(self.testable.data, None)
        self.assertEqual(self.messenger.data, None)
        self.assertEqual(self.filewriter.data, None)

        self.testable.publish_dictionary(self.data)
        self.messenger.publish_dictionary(self.data)
        self.filewriter.publish_dictionary(self.data)

        self.assertEqual(self.testable.data, self.data)
        self.assertEqual(self.messenger.data, self.data)
        self.assertEqual(self.filewriter.data, self.data)

    @patch('src.broadcaster.broadcaster.open')
    @patch('src.broadcaster.broadcaster.pub')
    def test_read_data(self, mock_open, mock_pub):
        """ Tests read data """
        self.testable.publish_dictionary(self.data)
        self.messenger.publish_dictionary(self.data)
        self.filewriter.publish_dictionary(self.data)

        self.assertEqual(self.testable.publish_key(key=1), "test")
        self.assertEqual(self.messenger.publish_key(key=2), "test2")
        self.assertEqual(self.filewriter.publish_key(key=3), "test3")
