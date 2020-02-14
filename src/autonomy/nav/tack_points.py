import math

from collections import deque

from numpy import sign

from src.gps_point import GPSPoint
from src.waypoint import Waypoint
from src.nav.strategy import favored_side


def place_tacks(start, end, boat, wind):
    """Places tacks between two waypoints.

    Algorithm description:
    If no tacks are required, add the last point and return.
    Otherwise
        Get favored side and confidence on [-1, 1]
        Set lateral boundaries on the beat (r_bound, l_bound)

        Set current_tack

        Set alpha to be the upwind angle of the boat
        Initialize r as upwind distance from start to end
        Initialize d as rhumbline distance

        Loop:
            If current_tack is port:
                If r_bound > current_pos.long:
                    Set x to r_bound
                    Set y to current_pos.lat + |x - current_pos.long| * tan(alpha)

                Else
                    Set x to l_bound
                    Set y to current_pos.lat - |x - current_pos.long| * tan(alpha)
                    Switch tacks
            If current_tack is starboard:
                If l_bound > current_pos.long:
                    Set x to l_bound
                    Set y to current_pos.lat - |x - current_pos.long| * tan(alpha)
                Else
                    Set x to r_bound
                    Set y to current_pos.lat + |x - current_pos.long| * tan(alpha)
                    Switch tacks

            Add (x, y) to tack points
            Set current_pos to (x, y)

            Set r to upwind distance to mark
            Set d to Cartesian distance to mark

            If arcsin(r/d) > alpha:
                break


    Keyword arguments:
    start -- The start of the leg
    end -- The end of the leg
    boat -- The boat sailing the course

    Returns:
    A list of waypoints.

    The first waypoint will be `start`, the second will be `end`."""
    tacks = deque()

    if start.must_tack_to_get_to(end, boat, wind):
        upwind_dist = wind.distance_upwind(start, end)
        bang_dist = upwind_dist * 0.5 * math.tan(math.radians(boat.upwind_angle))

        strategy = favored_side(wind)

        # The boat will tack between these two lines
        r_bound = bang_dist * 0.25 + 0.75 * strategy * bang_dist
        l_bound = bang_dist * -0.25 + 0.75 * strategy * bang_dist

        # 1 if on port tack, -1 if on starboard tack
        current_tack = sign(wind.angle_relative_to_wind(boat.current_heading))

        r = GPSPoint.distance(start, end)
        d = upwind_dist
        alpha = math.radians(math.fabs(boat.upwind_angle))
        current_pos = start

        while math.asin(r / d) > alpha:
            if current_tack is 1:
                if r_bound > current_pos.long:
                    x = r_bound
                    y = current_pos.lat + math.fabs(x - current_pos.long) * math.tan(alpha)
                else:
                    x = l_bound
                    y = current_pos.lat - math.fabs(x - current_pos.long) * math.tan(alpha)
                    current_tack *= -1
            elif current_tack is -1:
                if l_bound > current_pos.long:
                    x = l_bound
                    y = current_pos.lat - math.fabs(x - current_pos.long) * math.tan(alpha)
                else:
                    x = r_bound
                    y = current_pos.lat + math.fabs(x - current_pos.long) * math.tan(alpha)
                    current_tack *= -1
            else:
                break

            tacks.append(Waypoint(y, x))
            current_pos = Waypoint(y, x)
            r = wind.distance_upwind(current_pos, end)
            d = GPSPoint.distance(current_pos, end)

    tacks.append(end)
    return tacks


def must_tack_to_get_to(self, other, boat, wind):
    """Checks if tacks will be necessary to get to the other point from self"""
    bearing = wind.angle_relative_to_wind(other.bearing_from(self))
    return math.fabs(bearing) < boat.upwind_angle
