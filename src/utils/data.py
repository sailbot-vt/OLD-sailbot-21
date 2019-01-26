def constrain(val, min_val, max_val):
    """
    Method to constrain values to between the min_val and max_val.

    Keyword arguments:
    val -- The unconstrained value
    min_val -- The lowest allowed value
    max_val -- The highest allowed value
    """
    return min(max_val, max(min_val, val))
