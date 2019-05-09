import math
import sys

import numpy as np
import scipy.interpolate
import scipy.optimize

from src.utils.vec import Vec2

PATH_RESOLUTION = 10


def generate_path(world, boat, course):
    """Generates a navigation path from the starting point to the ending point.

    Keyword arguments:
    start -- The start point, a Vec2
    end -- The end point, a Vec2
    world -- A World object holding the current conditions
    boat -- A Boat object holding the boat design specifications

    Returns:
    An array of Vec2s along the routed path.
    """

    paths = []
    times = []

    # Choose n turn points
    for n_turns in range(find_max_reasonable_turns(course.current_leg.distance)):
        initial_turn_points = guess_turn_points(n_turns, course.current_leg)

        # Minimize time for the path between turn points
        res = scipy.optimize.minimize(time_for_path, initial_turn_points, args=(boat, world, course.current_leg))

        if res.success:
            paths += res.x
            times += time_for_path(res.x, boat, world, course.current_leg)

    # Find best path
    min_i = 0
    i = 0
    for time in times:
        if time < times[min_i]:
            min_i = i
        i += 1

    flat_path = paths[min_i]

    full_path = course.current_leg.start + flat_path + course.current_leg.end

    return build_path_from_turn_points(full_path)


def time_for_path(turn_points, boat, world, leg):
    """Estimates the total time for a path.

    The turn points are handled as a flat array for faster optimization.

    Keyword arguments:
    turn_points -- A flat array of points in 2d as [x0, y0, x1, y1, ...].

    Returns:
    An estimate of the time for the path defined by the turn points.
    """
    path = build_path_from_turn_points(leg.start + turn_points + leg.end)

    total_time_elapsed = 0.0
    prev_point = leg.start
    for point in path:
        heading = (point - prev_point).angle()
        d = (point - prev_point).length()
        v = boat.get_velocity(heading, world, total_time_elapsed)

        if v == 0:  # Will rarely happen, but handle it just in case
            return math.copysign(sys.float_info.max, d)

        total_time_elapsed += d / v  # est. time between prev point and point
        prev_point = point

    return total_time_elapsed


def build_path_from_turn_points(turn_points):
    """Builds path points in between turn points.

    Keyword arguments:
    turn_points -- A flat array of turn points, as [x0, y0, x1, y1, ...].

    Returns:
    An array of Vec2s that interpolate the turn points and minimizes each path
    in between the turn points.
    """
    path = []

    for i in range(0, len(turn_points) - 1, 2):
        subpath = []
        path_func = interpolate_straight_path([turn_points[i],
                                               turn_points[i + 1],
                                               turn_points[i + 2],
                                               turn_points[i + 3]])

        for t in range(PATH_RESOLUTION):
            subpath += Vec2(path_func(t / PATH_RESOLUTION))



        path += subpath

    return path


def interpolate_straight_path(flat_endpoints):
    """Interpolates two endpoints with a parameterized function.

    The t-range of the parameterized function is [0, 1]. If a value outside of
    that range is attempted, the call will fail.

    Keyword arguments:
    flat_endpoints -- The endpoints of the path, as [x0, y0, xf, yf]

    Returns:
    A function that gives the value of points on the path.
    """
    t_range = np.array([0, 1])
    endpoints = np.reshape(flat_endpoints, (2, 2))
    return scipy.interpolate.interp1d(t_range, endpoints, bounds_error=True)



def find_max_reasonable_turns(leg_distance):
    return 4


def guess_turn_points(n_turns, leg):
    return np.array([])
