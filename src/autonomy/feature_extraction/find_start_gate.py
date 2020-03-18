import numpy as np
from statistics import mean
from itertools import combinations as combs

from src.utils.coord_conv import polar_to_cartesian, cartesian_to_polar
from src.utils.polar_distance import polar_distance

def find_start_gate(buoy_array, config):
    """
    Identifies start gate given buoy array
    Inputs:
        buoy_array -- array made up of range and bearing data of buoys in tracker
        config -- contains start gate parameters
    Returns:
        centerpoint -- coordinates for centerpoint of start gate
        gate_buoys -- array of buoys comprising start gate
    """
    if len(buoy_array) > 0:
        width = config['width']
        variance = config['width_variance']

        # find buoy combinations
        buoy_combs = [comb for comb in combs(buoy_array, 2)]

        # find distance for each combination
        dists = np.array([polar_distance(buoy_comb) for buoy_comb in buoy_combs])

        # find combination with closest fit to width
        closest_fit_idx = np.abs(dists - width).argmin()

        if abs(dists[closest_fit_idx] - width) <= variance:
            return _find_centerpoint(buoy_combs[closest_fit_idx]), buoy_combs[closest_fit_idx]

    return None, None

def _find_centerpoint(buoy_array):
    """
    Finds centerpoint between two (start gate) buoys
    Inputs:
        buoy_array -- buoys to find centerpoint between
    Returns:
        centerpoint -- coordinates of centerpoint
    """
    # convert buoys to cartesian
    cart_buoys = [polar_to_cartesian(r, theta) for (r, theta) in buoy_array]
    
    # find cartesian centerpoint
    centerpoint = (mean((cart_buoys[0][0], cart_buoys[1][0])), mean((cart_buoys[0][1], cart_buoys[1][1])))

    # convert centerpoint to polar and return
    return cartesian_to_polar(*centerpoint)
