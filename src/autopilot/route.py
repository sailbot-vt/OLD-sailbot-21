from collections import deque


class Route:
    """Stores information about a route in terms of waypoints."""

    @property
    def current_waypoint(self):
        """The current waypoint"""
        return self.waypoints[0]

    def __init__(self):
        """Builds an empty route"""
        self.waypoints = deque()

    def update(self, waypoint):
        """Adds a waypoint to the route"""
        self.waypoints.append(waypoint)

    def next_waypoint(self):
        """Removes a waypoint from the route"""
        if len(self.waypoints) > 0:
            return self.waypoints.popleft()

        return None

    def __add__(self, other):
        """Concatenates two routes"""
        while len(other.waypoints) > 0:
            self.waypoints.append(other.waypoints.popleft())

    def add_waypoints(self, waypoints):
        """Adds waypoints (stored in a deque) to the route"""
        while len(waypoints) > 0:
            self.waypoints.append(waypoints.popleft())
