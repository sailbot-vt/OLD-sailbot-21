from flask_socketio import Namespace, emit


class CaptainSocket(Namespace):

    def __init__(self, captain, Namespace=None):
        super().__init__(Namespace)
        self.captain = captain