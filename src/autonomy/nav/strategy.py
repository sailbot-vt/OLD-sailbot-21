def favored_side(boat, wind):
    """Calculates the favored side of the course.

    A value of -1 indicates that the left side will be favored. A value of 0
    indicates that the leg will be evenly favored. A value of 1 indicates that
    the right side will be favored.

    Keyword arguments:
    boat -- the boat
    wind -- The wind

    Returns:
    A value between -1 and 1, indicating the confidence that the left or right
    side of the course, respectively, will be favored.
    """
    return -1 * wind.true_wind_angle / boat.upwind_angle
