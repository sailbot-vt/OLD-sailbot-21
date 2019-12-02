import numpy as np

def get_course_from_buoys(buoy_array, direction):
    """Returns a sorted array of buoys

     Inputs:
            buoy_array -- array made up of bearing and range data for each object in range inputted
            direction -- String to determine in what direction the array should be sorted in

        Returns:
            buoy_array -- array made up of bearing and range data for each object in range inputted
        """

    # Sorts the buoy array by bearing value
    sorted_array = np.sort(buoy_array, order="bearing")

    if direction == "CCW":
        return sorted_array
    else:
        return np.flipud(sorted_array)
