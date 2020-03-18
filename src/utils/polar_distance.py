import numpy as np

def polar_distance(pair):
    """
    Computes distance between two polar coordinates
    Inputs:
        pair -- pair of polar coords
    Returns:
        dist -- distance
    """
    p1, p2 = pair
    return np.sqrt(p1[0]**2 + p2[0]**2 - 2*p1[0]*p2[0]*np.cos(np.radians(p2[1] - p1[1])))
