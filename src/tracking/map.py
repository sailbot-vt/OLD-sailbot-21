from threading import Thread, Lock
from time import sleep

from pubsub import pub

from src.tracking.object import Object
from src.tracking.classification_types import ObjectType

from src.utils.coord_conv import cartesian_to_polar, polar_to_cartesian
from src.utils.time_in_millis import time_in_millis

import numpy as np

#TODO: add thread control back in
mutex = Lock()
class Map(Thread):
    """
    Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where
    our boat is, so each calculation should never have an absolute position in mind.
    """

    def __init__(self, boat, toggle_update):
        """ Initializes Map (done on startup) """
        super().__init__()
        pub.subscribe(self.add_object, "object detected")

        self.boat = boat
        self.object_list = []

        self.update_interval = 1
        self.toggle_update = toggle_update
        self.old_position = self.boat.current_position()

    def run(self):
        """ Continuously updates objects in object list using Kalman filter prediction"""
        while True:
            if toggle_update:
                self.update_map()
                sleep(self.update_interval)

    def enable_update(self):
        """Enables object updating using kalman filter"""
        self.toggle_update = True

    def disable_update(self):
        """Disables object updating using kalman filter"""
        self.toggle_update = False

    def add_object(self, delta_x, delta_y, objectType=ObjectType.NONE):
        """ Creates object for detection that is made to be added to map

        Inputs:
            delta_x -- Relative x position of object from boat (in m)
            delta_y= -- Relative y position of object from boat (in m)
            lastSeen -- Time object was last seen (in ms)
            objectType -- Classification of object (None for unclassified object)
        """
        # TODO: CHECK IF OBJECT FITS PRIOR TRACK (within threshold of object on list)
        if 0:  # if object fits prior track that is made, add object to track
            pass
        else:
            rng, bearing = cartesian_to_polar(delta_x, delta_y)
            new_object = Object(bearing, rng, time_in_millis(), objectType=objectType)
            self.object_list.append(new_object)

    def return_objects(self, bearingRange=[-30,30], timeRange=[0,5000], rngRange=None):
        """ Returns objects passing within given bearing range of boat in given time range

        Inputs:
            bearingRange -- Angle (in degrees) from bow to search within (0 to 360)
            timeRange -- Time (in ms) to search within using current boat velocity
            rngRange -- Range (in m) from bow to search within 
        
        Returns:
            return_list -- list made up of objects fitting criteria specified
        """
        _max_objs = 10               # Maximum number of objects to output (arbitrary choice)
        return_list = [0] * _max_objs

        if rngRange == None:
            # Convert time range to range range
            current_speed = self.boat.current_speed()
            rngRange = [(current_speed * (time_val/1000.)) for time_val in timeRange]

        ii = 0
        for obj in self.object_list:
            if ii >= 10:
                break
            if (rngRange[0] <= obj.rng <= rngRange[1] and (bearingRange[0] <= obj.bearing <= bearingRange[1])):
                return_list[ii] = obj
                ii += 1

        return return_list[0:ii]

    def get_buoys(self):
        """Returns buoys that are tracked in the map

        Returns:
            return_list -- list made up of buoys in map
        """

        # Create output array
        _max_objs = 5               # Maximum number of objects to output (arbitrary choice)
        return_list = [0] * _max_objs

        num_buoys = 0
        for ii, obj in enumerate(self.object_list):
            if num_buoys >= 5:
                break
            if obj.objectType == ObjectType.BUOY:
                return_list[num_buoys] = obj
                num_buoys += 1

        return return_list[0:num_buoys]

    def update_map(self):
        """ Updates map using boat state data"""
        position = self.boat.current_position()
        for object in self.object_list:
            object.predict()
        self.old_position = position

    def clear_objects(self, timeSinceLastSeen=0):
        """ Clears object from objects with greater than <timeSinceLastSeen> time since last seen

        Inputs:
            timeSinceLastSeen -- time since to exclude objects last seen time (in milliseconds)
        """

        cur_time = time_in_millis()
        del_list = []
        for ii, obj in enumerate(self.object_list):
            if (time_in_millis() - obj.lastSeen) > timeSinceLastSeen:
                del_list.append(ii)
        for index in sorted(del_list, reverse=True):
            del self.object_list[index]

