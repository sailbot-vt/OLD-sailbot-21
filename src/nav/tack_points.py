import math

from collections import deque


def place_tacks(start, end, boat, wind):
    """Places tacks between two waypoints

    Keyword arguments:
    start -- The start of the leg
    end -- The end of the leg
    boat -- The boat sailing the course

    Returns:
    A list of waypoints.

    The first waypoint will be `start`, the second will be `end`."""
    tacks = deque()

    if start.must_tack_to(end, boat, wind):
        # place tacks
        return -1

    tacks.append(end)
    return tacks


def must_tack_to(self, other, boat, wind):
    """Checks if tacks will be necessary to get to the other point from self"""
    bearing = wind.angle_relative_to_wind(other.bearing_from(self))
    return math.fabs(bearing) < boat.upwind_angle
