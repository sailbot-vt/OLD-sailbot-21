import numpy as np

def cartesian_to_polar(x, y):
    """Converts cartesian coordinates to range and bearing"""

    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x) * (180 / np.pi)      # get angle in degrees from -180 to 180

    return(r, theta)

def polar_to_cartesian(rng, bearing):
    """Converts range and bearing to cartesian coordinates"""
    rad_bearing = bearing * (np.pi/180.)
    x = rng*np.cos(rad_bearing)
    y = rng*np.sin(rad_bearing)
    return (x,y)
