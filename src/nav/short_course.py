import numpy as np
import scipy.optimize


PATH_RESOLUTION = 100


def generate_path(
        start,
        end,
        world,
        boat
):
    """Generates a navigation path from the starting point to the ending point.

    Keyword arguments:
    start -- The start point, a Vec2
    end -- The end point, a Vec2
    world -- A World object holding the current conditions
    boat -- A Boat object holding the boat design specifications

    Returns:
    An array of Vec2s along the routed path
    """

    # Choose n tack points
    for n_tacks in range(find_max_reasonable_tacks()):
        initial_tack_points = guess_tack_points()

        # Generate a corresponding path

        # Minimize time for the path
        scipy.optimize.minimize(time_for_path, initial_tack_points)

    # Find best path

    # Unflatten the path and return it
    pass


def time_for_path(tack_points):
    """Estimates the total time for a path.

    The tack points are handled as a flat array for faster optimization.

    Keyword arguments:
    tack_points -- A flat array of points in 2d.

    Returns:
    An estimate of the time for the path defined by the tack points.
    """
    path = build_path_from_tack_points(tack_points)

    pass


def build_path_from_tack_points(tack_points):
    """Interpolates points in between tack points."""

    return np.array([])


def unflatten_path(flat_path):
    """Generates a path of Vec2s from a flat path."""
    pass


def find_max_reasonable_tacks():
    return 4


def guess_tack_points():
    return np.array([])
