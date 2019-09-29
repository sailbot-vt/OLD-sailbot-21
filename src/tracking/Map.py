import datetime
from . import KalmanFilter

"""
Map is used to create a model of where objects around the boat currently exist. Everything is currently relative to where 
our boat is, so each calculation should never have an absolute position in mind.


"""
class Map():


    def __init__(self):
        self.objectList = []


    def add_object(self, bearing, distance, isBuoy = False, isBoat = False, approachSpeed = 0, angularSpeed = 0):
        newObject = object(bearing, distance, datetime.datetime.now(), isBuoy, isBoat, approachSpeed, angularSpeed)
        self.objectList.append(newObject)

    def updateObject(self, bearing, distance, speed, isBuoy = None, isBoat = None):
        for object in self.objectList:
            pass
            #object.KalmanFilter.update()
            #Find kalman filter predictions for all of our detected objects and update the one closest to our new update


    class Object():

        def __init__(self, bearing, distance, lastSeen, isBuoy, isBoat, approachSpeed, angularSpeed):
            self.bearing = bearing
            self.distance = distance
            self.lastSeen = lastSeen
            self.isBuoy = isBuoy
            self.isBoat = isBoat
            self.approachSpeed = approachSpeed
            self.angularSpeed = angularSpeed
            self.KalmanFilter = KalmanFilter()





