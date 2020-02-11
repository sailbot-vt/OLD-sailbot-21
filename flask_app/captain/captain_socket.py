from flask_socketio import Namespace, emit


class CaptainSocket(Namespace):

    def __init__(self, captain, Namespace=None):
        super().__init__(Namespace)
        self.captain = captain

    def switch_mode(self):
        self.captain.switch_mode()

    def drop_mark(self):
        self.captain.drop_mark()

    def clear_course(self):
        self.captain.clear_course()