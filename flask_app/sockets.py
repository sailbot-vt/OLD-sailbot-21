from flask_socketio import Namespace, emit

from flask_app.boat.boat_socket import BoatSocket
from flask_app.logger.logger_socket import LoggerSocket
from flask_app.captain.captain_socket import CaptainSocket
        

def apply_sockets(app, **kwargs):
    """ Applies multiplexed socket to the flask app.

    Keyword arguments:
    app - The Flask-socketio app to apply the sockets.

    **kwargs - Applies sockets based on keyword arguments given.
        valid kwargs: boat, world, captain, logger, rc_thread
    """
    if 'boat' in kwargs:
        app.on_namespace(BoatSocket(Namespace='/boat', boat=kwargs['boat']))
    if 'logger' in kwargs:
        app.on_namespace(LoggerSocket(Namespace='/logger', logger=kwargs['logger']))
    if 'world' in kwargs:
        # world socket
        pass
    if 'captain' in kwargs:
        app.on_namespace(CaptainSocket(Namespace='/captain', captain=kwargs['captain']))
    if 'rc_thread' in kwargs:
        # RC Socket
        pass