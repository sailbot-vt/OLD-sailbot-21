import numpy as np

from src.autonomy.nav.strategy import favored_side

from src.utils.coord_conv import polar_to_cartesian, cartesian_to_polar
from src.utils.polar_distance import polar_distance

def place_tacks(waypoint, boat, wind, config):
    """
    Places tacks between current position and waypoint
    Inputs:
        waypoint -- range and bearing (relative to boat position) of desired endpoint
        boat -- boat state object
        wind -- wind state object
        config -- tack configuration
    Returns:
        tacks -- list of tack waypoints (rng and bearing)
    """
    # get configuration params
    max_tacks = config['max_tacks']

    # initialize tacks
    tacks = []
    if must_tack(waypoint, boat, wind):
        # get favored side
        strategy = favored_side(boat, wind)

        # create tack channel (place l/r boundaries)
        upwind_dist = wind.distance_upwind((0, 0), waypoint)
        l_bound, r_bound = find_beating_bounds(upwind_dist, boat.upwind_angle, strategy)

        # find current tack
        current_tack = np.sign(wind.angle_relative_to_wind(boat.current_heading))

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
            if current_tack == 1:        # starboard tack
                tacks_cart[ii] = (cur_pos_cart[0] + (np.tan(upwind_rad) * (r_bound - cur_pos_cart[1])), r_bound)
                current_tack *= -1
            elif current_tack == -1:       # port tack
                tacks_cart[ii] = (cur_pos_cart[0] + (np.tan(upwind_rad) * (cur_pos_cart[1] - l_bound)), l_bound)
                current_tack *= -1

            # prepare for next loop
            cur_pos_cart = tacks_cart[ii]
            cur_pos = cartesian_to_polar(cur_pos_cart[0], cur_pos_cart[1])

            # calculate marginal absolute and upwind distance
            d_abs = polar_distance((cur_pos, (upwind_dist, 0)))
            d_up = wind.distance_upwind(cur_pos, (upwind_dist, 0))

            ii += 1

        # convert coordinates to cartesian and rotate based on wind angle
        tacks = [cartesian_to_polar(x, y) for (x, y) in tacks_cart[0:ii]]
        tacks = [(rng, bearing + wind.angle_relative_to_wind(boat.current_heading)) for (rng, bearing) in tacks]

    return tacks + [waypoint,]

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
