import json

from flask_socketio import Namespace, emit
from pubsub import pub


class BoatSocket(Namespace):

    def __init__(self, boat, Namespace=None):
        super().__init__(Namespace)
        self.boat = boat

    def current_position(self):
        return self.boat.current_position()

    def current_heading(self):
        return self.boat.current_heading()