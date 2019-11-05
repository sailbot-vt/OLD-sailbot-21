from threading import Thread, Lock
from time import sleep

from pubsub import pub

import datetime
from src.tracking.ExtendedKalmanFilter import EKF
from src.buoy_detection.Depth_Map_Calculator import Depth_Map
from src.tracking.KalmanFilter import KalmanFilter
from src.tracking.classification_types import ObjectType
import numpy as np
import math


class Map(Thread):
    """
    Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where
    our boat is, so each calculation should never have an absolute position in mind.
    """

    def __init__(self, boat, update_map):
        """ Initializes Map (done on startup) """
        super().__init__()
        self.is_active = True

        pub.subscribe(self.add_object, "buoy detected")

        self.boat = boat

        self.objectList = []
        self.depthCalc = Depth_Map()

        self.update_interval = 50
        self.update_map = update_map
        self.old_position = self.boat.current_position()

    def run(self):
        """ Continuously updates objects in object list using Kalman filter prediction"""
        while True:
            if update_map:
                self.updateMap()
            sleep(self.update_interval)

    def enable_update(self):
        """Enables object updating using kalman filter"""
        self.update_map = True

    def disable_update(self):
        """Disables object updating using kalman filter"""
        self.update_map = False

    def add_object(self, delta_x, delta_y, objectType=ObjectType.NONE, rangeRate=0, bearingRate=0):
        """ Creates object for detection that is made to be added to map

        Inputs:
            delta_x -- Relative x position of object from boat (in m)
            delta_y= -- Relative y position of object from boat (in m)
            lastSeen -- Time object was last seen (in ms)
            objectType -- Classification of object (None for unclassified object)
            rangeRate -- Velocity of object in radial direction (in m/s, + for object moving outwards)
            bearingRate -- Velocity of object in angular direction (in deg/s, + for object moving CCW)
        """
        if 0:  # if object fits prior track that is made, add object to track
            pass
        else:
            newObject = Object(delta_x, delta_y, datetime.datetime.now(), rangeRate, bearingRate, objectType)
            mutex.acquire()
            self.objectList.append(newObject)
            mutex.release()


    def cartesian_to_polar(self, x, y):
        r = math.sqrt(x^2 + y^2)
        theta = np.atan2(x/y) * (180/np.pi)

        return (theta, r)

    def return_objects(self, bearingRange=[-30,30], timeRange=[0,5000]):
        """ Returns objects passing within given bearing range of boat in given time range

        Inputs:
            bearingRange -- Angle (in degrees) from bow to search within
            timeRange -- Time (in ms) to search within using current boat velocity
        
        Returns:
            objectArray -- array made up of bearing, range, and classification data for each object in range inputted
        """
        # Create output array
        _max_objs = 10              # Maximum number of objects to output (arbitrary choice)
        _num_fields = 3             # Range, bearing, classification (using classification enum)
        objectArray = np.zeros(_max_objs, _num_fields)
        # Convert time range to range range
        current_speed = boat.current_speed()
        rngRange = [(current_speed * time_val) for time_val in timeRange]
        ii = 0
        mutex.acquire()
        for obj in self.objectList:
            if ii >= 10:
                break
            if (obj.range >= rngRange[0] and obj.range <= rngRange[1]) and (obj.bearing >= bearingRange[0] and obj.bearing <=bearingRange[1]):
                objectArray[ii] = np.array(obj.range, obj.bearing, obj.objectType)
                ii += 1
        mutex.release()

        return objectArray[0:ii]

    def get_buoys(self):
        """Returns buoys that are tracked in the map

        Returns:
            objectArray -- array made up of bearing, range, and classification data for each object in range inputted
        """
    
        # Create output array
        _max_objs = 5               # Maximum number of objects to output (arbitrary choice)
        _num_fields = 3             # Range, bearing, classification (using classification enum)
        objectArray = np.zeros(_max_objs, _num_fields)
        mutex.acquire()
        for ii, obj in enumerate(objectList):
            if obj.objectType == ObjectType.BUOY:
                objectArray[ii] = np.array(obj.range, obj.bearing, obj.objectType)
        mutex.release()

        return objectArray[0:ii]

    def polar_to_cartesian(self, bearing, range):
        x = range*math.cos(bearing)
        y = range*math.sin(bearing)
        return (x,y)

    def updateMap(self):
        """ Updates map using boat state data"""
        position = self.boat.current_position()
        mutex.acquire()
        for object in self.objectList:
            x,y = self.polar_to_cartesian(object.bearing, object.range)
            boat_x_moved, boat_y_moved = (position.y - old_position.y), (position.x - old_position.x)
            x -= boat_x_moved
            y -= boat_y_moved
            object.range, object.bearing = self.cartesian_to_polar(x, y)
        mutex.release()
        self.old_position = position

    def clear_objects(self, timeSinceLastSeen=0):
        """ Clears object from objects with greater than <timeSinceLastSeen> time since last seen

        Inputs:
            timeSinceLastSeen -- time (in ms) since to exclude objects last seen time
        """

        cur_time = datetime.datetime.now()
        del_list = []
        mutex.acquire()
        for ii, obj in enumerate(self.objectList):
            if (cur_time - obj.lastSeen) > timeSinceLastSeen:
                del_list.append(ii)
        for index in sorted(del_list, reverse=True):
            del self.objectList[index]
        mutex.release()

class Object():

    def __init__(self, bearing, range, lastSeen, rangeRate, bearingRate, objectType=ObjectType.NONE):
        """ Initalizes object that tracks a detection in map

        bearing -- Relative angle of object (in deg)
        rng -- Range of object from boat (in m)
        lastSeen -- Time object was last seen (in ms)
        objectType -- Classification of object (None for unclassified object)
        rangeRate -- Velocity of object in radial direction (in m/s, + for object moving outwards)
        bearingRate -- Velocity of object in angular direction (in deg/s, + for object moving CCW)
        """
        self.bearing = bearing
        self.range = range
        self.lastSeen = lastSeen
        self.objectType = objectType
        self.rangeRate = rangeRate
        self.bearingRate = bearingRate

        dt = 1.0 / 60
        F = None
        H = None
        O = None
        R = None

        # We will want different prediction calibrations for a buoy vs a boat
        if objectType is "Buoy":
            F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
            H = np.array([1, 0, 0]).reshape(1, 3)
            Q = np.array([[0.05, 0.05, 0.0], [0.05, 0.05, 0.0], [0.0, 0.0, 0.0]])
            R = np.array([0.5]).reshape(1, 1)
        else:
            F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
            H = np.array([1, 0, 0]).reshape(1, 3)
            Q = np.array([[0.05, 0.05, 0.0], [0.05, 0.05, 0.0], [0.0, 0.0, 0.0]])
            R = np.array([0.5]).reshape(1, 1)

        self.kalman = KalmanFilter(F=F, H=H, Q=Q, R=R)


class LinearPrediction():

    def __init__(self, initial_xy_measurements):
        pass
