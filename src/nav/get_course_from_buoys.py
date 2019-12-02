import numpy as np

def get_course_from_buoys(buoy_array, direction):
    """Returns a sorted array of buoys

     Inputs:
            buoy_array -- array made up of bearing and range data for each object in range inputted
            direction -- String to determine in what direction the array should be sorted in

     Returns:
            sorted_array -- array made up of bearing and range data for each object in range inputted
        """

    # Sorts the buoy array by bearing value
    if (buoy_array['bearing'] >= 180).any():        # if boat is inside of bounding polygon made by buoys
        sorted_array = sort_inside_polygon(buoy_array)
    else:                                          # if boat is outside of bounding polygon
        sorted_array = np.sort(buoy_array, order="bearing")

    if direction == "CCW":
        return sorted_array
    else:
        return np.flipud(sorted_array)

def sort_inside_polygon(coord_array):
    """Returns a sorted array accounting for boat being inside polygons

    Inputs:
        coord_array -- array of polar coordinates (structured array)

    Returns:
        sorted_array -- sorted array accounting for boat being inside polygons
    """

    # include original indices in sorted array
    inc_index_dtype = np.dtype(coord_array.dtype.descr + [('index', int)])
    indexed_array = np.zeros(coord_array.shape, dtype=inc_index_dtype)
    indexed_array['range'] = coord_array['range']
    indexed_array['bearing'] = coord_array['bearing']
    indexed_array['index'] = np.array([range(coord_array.size)])

    # shift radially
    for ii in range(indexed_array.size):
        if indexed_array[ii]['bearing'] < 270:
            indexed_array[ii]['bearing'] += 90
        else:
            indexed_array[ii]['bearing'] = -1 * (indexed_array[ii]['bearing'] - 360)
    
    # sort array by bearing
    sorted_indexed_array = np.sort(indexed_array, order='bearing')

    print("\n")
    print(coord_array[sorted_indexed_array['index']])

    return coord_array[sorted_indexed_array['index']]
