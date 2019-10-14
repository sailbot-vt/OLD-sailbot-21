from flask_socketio import emit

from flask_app.airmar.airmar_socket import AirmarSocket


def apply_sockets(app):
    """ Applies multiplexed socket to the flask app.

    Keyword arguments:
    app - The Flask-socketio app to apply the sockets.
    """
    # Start serializations for sockets
    AirmarSocket() 

    @socketio.on('airmar_data', namespace='/airmar')
    def broadcast_airmar_data():
        emit('my response', {'data': AirmarSocket.serialized_data()})