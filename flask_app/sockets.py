from flask_socketio import Namespace, emit

from flask_app.boat.boat_socket import BoatSocket
from flask_app.logger.logger_socket import LoggerSocket


def apply_sockets(app):
    """ Applies multiplexed socket to the flask app.

    Keyword arguments:
    app - The Flask-socketio app to apply the sockets.
    """
    app.on_namespace(BoatSocket('/boat'))
    app.on_namespace(LoggerSocket('/logger'))