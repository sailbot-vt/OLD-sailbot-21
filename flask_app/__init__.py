from flask import Flask, render_template
from flask_socketio import SocketIO

from flask_app.routes import apply_routes
from flask_app.sockets import apply_sockets

def create_app(test_config=None):
    """" Builds the Flask app.

    Keyword Arguments:
    test_config - An optional test configuration for testing.

    Returns:
    the flask application
    """

    app = Flask(__name__)
    # TODO Hide secret.
    app.config['SECRET_KEY'] = 'secret!'

    apply_routes(app)

    return app

def create_socket(app, **kwargs):
    """ Builds the SocketIO from flask app.

    Keyword Arguments:
    app - The Flask app

    Returns:
    The socketio wrapper
    """
    socketio = SocketIO(app)
    apply_sockets(socketio, **kwargs)

    return socketio
