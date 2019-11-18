from threading import Thread, Lock
from src.boat.boat import Boat
from src.tracking.Map import Map
from src.tracking.Map import Object
import src.tracking.map as map
import math


def run(buoy_array, boat_position, boat_heading, direction):
    buoys = buoy_array
    direction = direction
    position = boat_position
    heading = boat_heading
    # Traverse through all array elements
    if direction == "CCW":

        firstpoint = min(buoys.bearing)
        index = buoys.index(min(buoys))
        temp = buoys[0]
        buoys[0] = buoys[index]
        buoys[index] = temp

        for i in range(len(buoys)):

            # Find the minimum element in remaining
            # unsorted array
            min_idx = i + 1
            counter = 0
            # if buoys.bearing[min_idx] < 90:

            for j in range(i + 1, len(buoys)):
                min_idx = j
                distance1 = math.sqrt(buoys.range[min_idx] * buoys.range[min_idx] + buoys[0].range * buoys[0].range
                                      - 2 * buoys[0].range * buoys.range[min_idx] * math.cos(buoys.bearing[min_idx] -
                                                                                             buoys[0].bearing))
                distance2 = math.sqrt(buoys.range[j] * buoys.range[j] + buoys[0].range * buoys[0].range
                                      - 2 * boat_position * buoys.range[j] * math.cos(buoys.bearing[j] -
                                                                                      buoys[0].bearing))
                if distance1 > distance2:
                    min_idx = j
            #  Swap the found minimum element with
            # the first element
            buoys[i], buoys[min_idx] = buoys[min_idx], buoys[i]
