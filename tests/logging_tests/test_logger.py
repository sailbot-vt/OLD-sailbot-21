import unittest
from pubsub import pub

from src.logging.logger import Logger


class LoggerTests(unittest.TestCase):
    """Tests methods in Logger"""

    def setUp(self):
        """Create Logger object"""
        self.logger = Logger()

    def test_write_msg(self):
        """Tests that logger receives messages correctly"""

        pub.sendMessage('write msg', pin_name='test', msg='testing', rw_state='r')
        log_dict = self.logger.log_dict
        assert(log_dict['pin_name'] == 'test')
        assert(log_dict['msg'] == 'testing')
        assert(log_dict['r/w'] == 'r')
