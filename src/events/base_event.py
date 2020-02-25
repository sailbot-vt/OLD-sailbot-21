from abc import ABC, abstractmethod

from threading import Thread, Lock
from pubsub import pub

from src.navigation_mode import NavigationMode
from src.nav.course import ObjectCourse

mutex = Lock()

class Event(ABC, Thread):
    """Base event type"""

    def __init__(self):
        """Creates a new event"""
        Thread.__init__()

        self.is_active = True
        self.read_interval()

        self.course = ObjectCourse()
        
        pub.subscribe(self.switch_mode, "set nav mode")

    @abstractmethod
    def run(self):
        """Runs event thread"""

    @abstractmethod
    def read_interval(self):
        """Reads update interval from config"""
        pass

    def switch_mode(self, mode):
        """
        Changes the navigation mode
        Inputs:
            mode -- navigation mode to switch to
        """
        if mode is NavigationMode.AUTONOMOUS:
            self.enable()
        else:
            self.disable()

    def enable(self):
        """Enables autonomous navigation"""
        self.is_active = True

    def disable(self):
        """
        Disable autonomous navigation
        Side Effects:
            course -- clears course
        """   
        self.is_active = False
        self.course.clear()

    def add_object(self, obj):
        """
        Adds waypoint at object
        Side Effects:
            course -- adds object to course
        """
        mutex.acquire()
        self.course.add_obj(obj)
        mutex.release()

    def clear_course(self):
        """
        Clears course of all obejcts 
        Side Effects:
            course -- clears course
        """
        mutex.acquire()
        self.course.clear()
        mutex.release()

    def create_objectives(self):
        """
        Creates objectives based on enumerations
        """
        return []

