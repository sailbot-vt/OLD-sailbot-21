from pubsub import pub

from src.autopilot.route import Route


class Autopilot:
    """Manages the steering of the boat in autonomous mode."""

    def __init__(self):
        """Builds a new autopilot."""
        self.route = Route()
        pub.subscribe(self.route.update, "waypoints")
