import os
import unittest
import parse

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
            "1" : "test1",
            "2" : "test2",
            "3" : "test3"
        }

    @patch('src.broadcaster.broadcaster.pub', autospec=True)
    def test_update_data(self, mock_pub):
        """ Tests update data for broadcasters """
        self.testable.publish_dictionary(self.data)
        self.messenger.publish_dictionary(self.data)
        self.filewriter.publish_dictionary(self.data)

        # Local storage 
        self.assertEqual(self.testable.data, self.data)

        # Pubsub
        mock_pub.sendMessage.assert_any_call(topicName="1", msgData="test1")
        mock_pub.sendMessage.assert_any_call(topicName="2", msgData="test2")
        mock_pub.sendMessage.assert_any_call(topicName="3", msgData="test3")

        # File
        f = open(self.filewriter.filename, "r")
        lines = f.readlines() 
        # Since dictionary keys may not be published in order,
        # we have to store the key-value pairs from file to temp dictionary
        # for testing purposes.
        line_format = "[{0}]\t\t[Requested: {1} -- Data: {2}]\n"

        res_dict = dict()
        for line in lines:
            parsed = parse.parse(line_format, line)
            res_dict[parsed[1]] = parsed[2]
        self.assertEqual(self.data, res_dict)