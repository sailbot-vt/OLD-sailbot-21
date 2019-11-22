import numpy as np


def get_course_from_buoys(buoy_array, direction):
    """Returns a sorted array of buoys

     Inputs:
            buoy_array -- array made up of bearing, range, and classification data for each object in range inputted
            direction -- String to determine in what direction the array should be sorted in

        Returns:
            buoy_array -- array made up of bearing, range, and classification data for each object in range inputted
        """

    # Sorts the buoy array by bearing value
    np.sort(buoy_array, order=buoy_array.bearing)

    if direction == "CCW":
        return buoy_array
    else:
        return np.flipud(buoy_array)
