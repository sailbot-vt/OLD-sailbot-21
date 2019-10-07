import datetime
from . import KalmanFilter

class Map():
    """
    Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where 
    our boat is, so each calculation should never have an absolute position in mind.
    """

    def __init__(self):
        """ Initializes Map (done on startup) """
        self.objectList = []


    def add_object(self, bearing, rng, objectType = None, rangeRate = 0, bearingRate = 0):
        """ Creates object for detection that is made to be added to map

        bearing -- Relative angle of object (in deg)
        rng -- Range of object from boat (in m)
        lastSeen -- Time object was last seen (in ms)
        objectType -- Classification of object (None for unclassified object)
        rangeRate -- Velocity of object in radial direction (in m/s, + for object moving outwards)
        bearingRate -- Velocity of object in angular direction (in deg/s, + for object moving CCW)
        """
        
        if 0:           # if object fits prior track that is made, add object to track 
            pass
        else:
            newObject = object(bearing, rng, datetime.datetime.now(), objectType, rangeRate, bearingRate)
            self.objectList.append(newObject)

    def updateObject(self, bearing, rng, speed, objectType = None):
        for object in self.objectList:
            pass
            #object.KalmanFilter.update()
            #Find kalman filter predictions for all of our detected objects and update the one closest to our new update

class Object():

    def __init__(self, bearing, rng, lastSeen, objectType, rangeRate, bearingRate):
        """ Initalizes object that tracks a detection in map

        bearing -- Relative angle of object (in deg)
        rng -- Range of object from boat (in m)
        lastSeen -- Time object was last seen (in ms)
        objectType -- Classification of object (None for unclassified object)
        rangeRate -- Velocity of object in radial direction (in m/s, + for object moving outwards)
        bearingRate -- Velocity of object in angular direction (in deg/s, + for object moving CCW)
        """
            
        self.bearing = bearing
        self.rng = distance
        self.lastSeen = lastSeen
        self.isBuoy = isBuoy
        self.isBoat = isBoat
        self.rangeRate = rangeRate
        self.bearingRate = angularSpeed
        self.KalmanFilter = KalmanFilter()

