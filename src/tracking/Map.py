import datetime
from src.tracking.ExtendedKalmanFilter import EKF
from src.buoy_detection.Depth_Map_Calculator import Depth_Map
from src.tracking.KalmanFilter import KalmanFilter
import numpy as np


class Map:
    """
    Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where 
    our boat is, so each calculation should never have an absolute position in mind.
    """

    def __init__(self):
        """ Initializes Map (done on startup) """
        self.objectList = []
        self.depthCalc = Depth_Map()

    def add_object(self, bearing, range, objectType=None, rangeRate=0, bearingRate=0):
        """ Creates object for detection that is made to be added to map

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
            self.objectList.append(newObject)

    def updateObject(self, bearing, rng, speed, objectType=None):
        for object in self.objectList:
            pass
            # object.KalmanFilter.update()
            # Find kalman filter predictions for all of our detected objects and update the one closest to our new update

    def planar_to_radial(self):
        pass

    def radial_to_planar(self, bearing, range):
        pass


class Object():

    def __init__(self, bearing, range, lastSeen, objectType, rangeRate, bearingRate):
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
