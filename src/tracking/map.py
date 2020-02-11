from threading import Thread, Lock
from time import sleep

from pubsub import pub

from src.tracking.object import Object
from src.tracking.classification_types import ObjectType

from src.utils.time_in_millis import time_in_millis


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
        rng, bearing = cartesian_to_polar(delta_x, delta_y)
        obj_index = self._find_object_in_map(rng, bearing, objectType)
        if (obj_index != None):                     # if object fits prior track that is made, add object to track
            self.object_list[obj_index].update(rng, bearing)
        else:
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

    def _find_object_in_map(self, rng, bearing, obj_type):
        """Finds if object exists in map and returns object index if true, otherwise returns None
        Inputs:
            rng -- range of object detected
            bearing -- bearing of object detected
            obj_type -- type of object detected
        Returns:
            object_index -- index of object that matches track, none if no object matches
        """

        # init x and y ranges
        rng_range = [0] * 2
        bearing_range = [0] * 2

        # search through objects in object list
        for ii, obj in enumerate(self.object_list):
            # get newest prediction for object
            obj.predict()
            
            # find range around objects position
            rng_range[0] = obj.kalman.state[0] - obj.kalman.covar[0,0]
            rng_range[1] = obj.kalman.state[0] + obj.kalman.covar[0,0]

            bearing_range[0] = obj.kalman.state[1] - obj.kalman.covar[1,1]
            bearing_range[1] = obj.kalman.state[1] + obj.kalman.covar[1,1]

            # if detection is in uncertainty range of object and is same type (or unknown type)
            if (rng_range[0] <= rng <= rng_range[1]) and (bearing_range[0] <= bearing <= bearing_range[1]) and \
                                                   ((obj_type == obj.objectType) or (obj_type == ObjectType.NONE)):

                return ii

        return None
