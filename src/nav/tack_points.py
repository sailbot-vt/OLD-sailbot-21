def next_waypoint(course):
    """
    if (downwind)
        return course.next_mark_waypoint()

    for i < MAX_TACKS
        place tacks
        calculate risk
        estimate time

    choose best risk/time path
    return next tack point in that path
    """
    pass


def place_tacks(start, end):
    """Places tacks between two waypoints

    Keyword arguments:
    start -- The start of the upwind leg
    end -- The end of the upwind leg

    Returns:
    A list of beating waypoints.

    The first waypoint will be `start`, the second will be `end`."""
    pass
