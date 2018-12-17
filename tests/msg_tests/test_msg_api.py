import unittest
from time import sleep

import src.msg as msg


class TestMsgAPI(unittest.TestCase):
    """Tests the message system endpoints."""

    def setUp(self):
        """Runs before each test method."""
        self.msgs = []
        self.s1 = msg.Subscriber("channel name here", lambda data: self.msgs.append(data))
        self.s2 = msg.Subscriber("channel name here", lambda data: self.msgs.append(data))

    def test_msg(self):
        """Tests the subscribe function."""
        msg.publish("channel name here", "hi")
        sleep(0.01)
        assert self.msgs.count("hi") == 2


if __name__ == "__main__":
    unittest.main()
