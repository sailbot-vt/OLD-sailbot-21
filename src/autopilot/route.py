class Route:
    """Stores information about a route in terms of waypoints."""
    def __init__(self):
        """Builds an empty route"""
        self.waypoints = []

    def update(self, waypoint):
        """Adds a waypoint to the route"""
        self.waypoints.append(waypoint)
