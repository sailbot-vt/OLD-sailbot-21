from flask import Flask, render_template
from flask_socketio import SocketIO

from flask_app.routes import apply_routes

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

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    apply_routes(app)

    return app

def create_socket(app):
    """ Builds the SocketIO from flask app.

    Keyword Arguments:
    app - The Flask app

    Returns:
    the socketio
    """
    return SocketIO(app)

if __name__ == "__main__":
    app = create_app()
    socketio = SocketIO(app)
    socketio.run()