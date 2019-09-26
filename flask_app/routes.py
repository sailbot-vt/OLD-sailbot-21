def apply_routes(app):
    """ Applies URL routes to the flask app.

    Keyword arguments:
    app - The Flask app to apply the routes.
    """
    
    @app.route('/')
    def hello_world():
        return "Hello, world!"