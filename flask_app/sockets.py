from flask_socketio import Namespace, emit

from flask_app.airmar.airmar_socket import AirmarSocket


def apply_sockets(app):
    """ Applies multiplexed socket to the flask app.

    Keyword arguments:
    app - The Flask-socketio app to apply the sockets.
    """
    app.on_namespace(AirmarSocket('/airmar'))