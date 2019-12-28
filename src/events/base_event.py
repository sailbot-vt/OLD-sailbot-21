from abc import ABC, abstractmethod

from threading import Thread

class Event(ABC, Thread):
    """Base event type"""

    def __init__(self):
        """Creates a new event"""
        Thread.__init__()

    @abstractmethod
    def add_waypoint(self, obj):
        """Adds waypoint at object"""
        pass
