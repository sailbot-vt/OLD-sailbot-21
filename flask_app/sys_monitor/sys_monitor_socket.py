from flask_socketio import Namespace, emit


class SysMonitorSocket(Namespace):

    def __init__(self, Namespace=None):
        super().__init__(Namespace)
