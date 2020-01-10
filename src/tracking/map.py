from threading import Thread, Lock
from time import sleep

from pubsub import pub

from src.tracking.object import Object
from src.tracking.classification_types import ObjectType
from src.tracking.pdaf import joint_pdaf

from src.utils.coord_conv import cartesian_to_polar, polar_to_cartesian
from src.utils.time_in_millis import time_in_millis

import numpy as np

class Map(Thread):
    """
    Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where
    our boat is, so each calculation should never have an absolute position in mind.
    """

    def __init__(self, boat, toggle_update):
        """ Initializes Map (done on startup) """
        super().__init__()
        pub.subscribe(self.smooth_frame, "object(s) detected")

        self.boat = boat
        self.object_list = []

        self.update_interval = 0.5
        self.toggle_update = toggle_update
        self.old_position = self.boat.current_position()

    def run(self):
        """ Continuously updates objects in object list using Kalman filter prediction"""
        while self.toggle_update:
            self.update_map()
            self.prune_objects()
            sleep(self.update_interval)

    def enable_update(self):
        """Enables object updating using kalman filter"""
        self.toggle_update = True

    def disable_update(self):
        """Disables object updating using kalman filter"""
        self.toggle_update = False

    def smooth_frame(self, epoch_frame, frame_bounds):
        """
        Updates map using observations from object list input

        Inputs:
            epoch_frame  -- list containing rng, bearing, and object type for each detection in epoch
            frame_bounds -- tuple of lists containing range and bearing bounds

        Side Effects:
            object_list -- Updates object list using data from frame (updates or creates new objects)
        """
        # trim object list to only include tracks with frame bounds
        trimmed_object_list = self.return_objects(bearingRange = frame_bounds[1], rngRange = frame_bounds[0])

        # generate gate list
        gate_list = [self._generate_obj_gate(obj) for obj in trimmed_object_list]

        # get update list from joint pdaf
        update_list, detections_used = joint_pdaf(trimmed_object_list, gate_list, epoch_frame)

        for obj, update in zip(trimmed_object_list, update_list):
            # update objects
            if update is not None:
                obj.update(update[0], update[1])

        # use all detections NOT used to update objects to create new objects
        for ii, det in enumerate(epoch_frame):
            if detections_used[ii] == 0:
                new_obj = Object(det[1], det[0], time_in_millis(), objectType = det[2])     # create object using detection
                self.object_list.append(new_obj)        # add to object_list

    def prune_objects(self):
        """
        Prunes objects in object list
        """
        # iterate through objects in track
        for ii, obj in enumerate(self.object_list):
            num_updates = sum(filter(None, obj.updateHist))

            # prune tracks w/ updates in <= 0.4 * expected updates
            if num_updates <= (0.4 * obj.histLength):
                del self.object_list[ii]


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

    def _generate_obj_gate(self, obj):
        """
        Generates tuple containing gate around object
        Inputs:
            obj -- object to create gate around
        Returns:
            gate -- tuple containing range range, bearing range, and allowable object types
        """
        rng_gate = (obj.rng - obj.kalman.covar[0,0], obj.rng + obj.kalman.covar[0, 0])
        bearing_gate = (obj.bearing - obj.kalman.covar[1,1], obj.bearing + obj.kalman.covar[1, 1])
        type_gate = (ObjectType.NONE, obj.objectType)

        return (rng_gate, bearing_gate, type_gate)
