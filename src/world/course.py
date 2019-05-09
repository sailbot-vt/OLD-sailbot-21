class Course:
    """Stores information about a course."""
    def __init__(self, waypoints):
        """Builds a new course from the given waypoints.

        Keyword arguments:
        waypoints -- The waypoints for the new course.
        """
        self.waypoints = waypoints
        self.current_waypoint = -1

    def next_mark_waypoint(self):
        """Returns a waypoint at the next mark."""
        self.current_waypoint += 1
        return self.waypoints[self.current_waypoint]
