import numpy as np

from src.autonomy.nav.strategy import favored_side

from src.utils.coord_conv import polar_to_cartesian, cartesian_to_polar
from src.utils.polar_distance import polar_distance

def place_tacks(waypoint, boat, wind, config, switch_tack):
    """
    Places tacks between current position and waypoint
    Inputs:
        waypoint -- range and bearing (relative to boat position) of desired endpoint
        boat -- boat state object
        wind -- wind state object
        config -- tack configuration
        switch_tack -- flag to switch tack side
    Returns:
        tacks -- list of tack waypoints (rng and bearing)
    """
    # get configuration params
    max_tacks = config['max_tacks']

    # initialize tacks
    tacks = []
    if must_tack(waypoint, boat, wind):
        # get favored side
        strategy = favored_side(waypoint, boat, wind)

        # create tack channel (place l/r boundaries)
        upwind_dist = wind.distance_upwind((0, 0), waypoint)
        l_bound, r_bound = find_beating_bounds(upwind_dist, boat.upwind_angle, strategy)

        # find current tack
        tack_side = np.sign(wind.angle_relative_to_wind(boat.current_heading))
        if switch_tack:
            tack_side *= -1

        # find upwind angle, absolute distance
        upwind_rad = np.radians(np.fabs(boat.upwind_angle))
        d_abs = waypoint[0]

        # set up loop
        tacks_cart = [0] * max_tacks
        ii = 0
        cur_pos_cart = (0, 0)
        d_up = upwind_dist

        # loop until possible to get to waypoint without tacking again
        while (np.arcsin(d_up/ d_abs) > (upwind_rad+0.0001)) and (ii < max_tacks):      # allow slight undershoot
            if tack_side == 1:        # starboard tack
                tacks_cart[ii] = (cur_pos_cart[0] + (np.tan(upwind_rad) * np.fabs(r_bound - cur_pos_cart[1])), r_bound)
                tack_side *= -1
            elif tack_side == -1:       # port tack
                tacks_cart[ii] = (cur_pos_cart[0] + (np.tan(upwind_rad) * np.fabs(l_bound - cur_pos_cart[1])), l_bound)
                tack_side *= -1

            # prepare for next loop
            cur_pos_cart = tacks_cart[ii]
            cur_pos = cartesian_to_polar(cur_pos_cart[0], cur_pos_cart[1])

            # calculate marginal absolute and upwind distance
            d_abs = polar_distance((_bearing_offset(cur_pos, waypoint[1]), waypoint))
            d_up = wind.distance_upwind(_bearing_offset(cur_pos, waypoint[1]), waypoint)

            ii += 1

        # convert cartesian to polar and rotate based on waypoint bearing
        tacks = [cartesian_to_polar(x, y) for (x, y) in tacks_cart[0:ii]]
        tacks = [_bearing_offset(tack, waypoint[1]) for tack in tacks]

    return tacks

def find_beating_bounds(upwind_dist, upwind_ang, strategy):
    """
    Finds bounds for beating using upwind distance and strategy
    Inputs:
        upwind_dist -- distance upwind of object
        upwind_ang -- angle upwind of object
        strategy -- strategy of beating (from -1 to 1 for favoring port / starboard side)
    Returns:
        l_bound, r_bound -- left and right bounds of beating
    """
    bang_dist = upwind_dist * 0.5 * np.tan(np.radians(upwind_ang))

    r_bound = (bang_dist * 0.25) + (0.75 * strategy * bang_dist)
    l_bound = (bang_dist * -0.25) + (0.75 * strategy * bang_dist)

    return l_bound, r_bound
    

def must_tack(end, boat, wind):
    """Checks if tacks will be necessary to get to the other point from origin"""
    bearing = wind.angle_relative_to_wind(end[1])
    return np.fabs(bearing) < boat.upwind_angle

def _bearing_offset(coord, offset):
    """
    Applies bearing offset to polar coordinate
    Inputs:
        coord -- polar coordinate
        offset -- bearing offset
    Returns:
        offset_coord -- bearing offseted coordinate
    """
    return (coord[0], coord[1] + offset)
