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
    if (buoy_array[1] >= 180).any():        # if boat is inside of bounding polygon made by buoys
        sorted_array = sort_inside_polygon(buoy_array.view(np.float))
    else:                                          # if boat is outside of bounding polygon
        sorted_array = np.sort(buoy_array.view('f8, f8'), order='f1', axis=0).view(np.float)    # sort along bearing column

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
    adj_bearing_array = np.copy(coord_array[:, 1])

    # shift radially
    for ii in range(adj_bearing_array.shape[0]):
        if adj_bearing_array[ii] < 270:
            adj_bearing_array[ii] += 90
        else:
            adj_bearing_array[ii] = -1 * (adj_bearing_array[ii] - 360)

    # sort array by adjusted bearing
    return coord_array[adj_bearing_array.argsort()]
