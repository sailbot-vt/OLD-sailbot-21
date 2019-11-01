from threading import Thread, Lock
from time import sleep

from pubsub import pub

import datetime
from src.tracking.ExtendedKalmanFilter import EKF
from src.buoy_detection.Depth_Map_Calculator import Depth_Map
from src.tracking.KalmanFilter import KalmanFilter
from src.track.classification_types import ObjectType
import numpy as np
import math


class Map(Thread):
    """
    Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where
    our boat is, so each calculation should never have an absolute position in mind.
    """

    def __init__(self, boat):
        """ Initializes Map (done on startup) """
        super().__init__()
        self.is_active = True

        pub.subscribe(self.add_object, "buoy detected")

        self.boat = boat

        self.objectList = []
        self.depthCalc = Depth_Map()
        self.update_interval = 50


    def run(self):
        """ Continuously updates objects in object list using Kalman filter prediction"""
        while True:
            self.updateMap()
            sleep(self.update_interval)

    def add_object(self, bearing, range, objectType=ObjecttType.NONE, rangeRate=0, bearingRate=0):
        """ Creates object for detection that is made to be added to map

        Inputs:
            bearing -- Relative angle of object (in deg)
            rng -- Range of object from boat (in m)
            lastSeen -- Time object was last seen (in ms)
            objectType -- Classification of object (None for unclassified object)
            rangeRate -- Velocity of object in radial direction (in m/s, + for object moving outwards)
            bearingRate -- Velocity of object in angular direction (in deg/s, + for object moving CCW)
        """
        if 0:  # if object fits prior track that is made, add object to track
            pass
        else:
            newObject = object(bearing, range, datetime.datetime.now(), objectType, rangeRate, bearingRate)
            mutex.acquire()
            self.objectList.append(newObject)
            mutex.release()


    def cartesian_to_polar(self, x, y):
        r = math.sqrt(x^2 + y^2)
        theta = math.atan(x/y)

        # If in 2nd or 3rd quadrant
        if x < 0:
            theta += 180
        # If in 4th quadrant
        elif x > 0 and y < 0:
            theta += 360
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
        objectArray = np.zeros(10, 3)
        # Convert time range to range range
        current_speed = boat.current_speed()
        rngRange = [(current_speed * time_val) for time_val in timeRange]
        ii = 0
        mutex.acquire()
        for obj in objectList:
            if ii >= 10:
                break
            if (obj.range >= rngRange[0] and obj.range <= rngRange[1]) and (obj.bearing >= bearingRange[0] and obj.bearing <=bearingRange[1]):
                objectArray[ii] = np.array(obj.range, obj.bearing, obj.objectType)
                ii += 1
        mutex.release()

        return objectArray[0:ii]

    def polar_to_cartesian(self, bearing, range):
        x = range*math.cos(bearing)
        y = range*math.sin(bearing)
        return (x,y)

    def updateMap(self):
    """ Updates map using boat state data"""
        position = boat.current_position()
        mutex.acquire()
        for object in self.objectList:
            x,y = self.polar_to_cartesian(object.bearing, object.range)
            boat_x_moved, boat_y_moved = (position.y - old_position.y), (position.x - old_position.x)
            x -= boat_x_moved
            y -= boat_y_moved
            object.range, object.bearing = self.cartesian_to_polar(x, y)
        mutex.release()
        old_position = position


class Object():

    def __init__(self, bearing, range, lastSeen, objectType=ObjectType.NONE, rangeRate, bearingRate):
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
