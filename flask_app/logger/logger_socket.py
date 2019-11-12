import json
import datetime

from flask_socketio import Namespace, emit
from pubsub import pub


class LoggerSocket(Namespace):
    """ Process airmar data from pubsub """

    def __init__(self, logger, Namespace=None):
        super().__init__(Namespace)
        pub.subscribe(self.update_write_msg, "write msg")
        pub.subscribe(self.update_config_dict, "config dict")

    def update_write_msg(self, pin_name, msg, rw_state):
        """ Polls for last write message from logger from
        pubsub

        Returns:
        A string of last logger message.
        """

        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d // %H:%M:%S')
        log_dict = {'datetime': datetime_str, 'pin_name': pin_name, 'msg': msg, 'r/w' : rw_state} 

        return json.dumps(log_dict)

    def update_config_dict(self, config_dict):
        """ Polls for the last config.yml dictionary from
        pubsub

        Returns:
        A json pickled string representation of the config dict
        """
        return json.dumps(config_dict)