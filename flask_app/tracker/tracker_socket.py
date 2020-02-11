from flask_socketio import Namespace, emit


class TrackerSocket(Namespace):

    def __init__(self, tracker, Namespace=None):
        super().__init__(Namespace)
        self.tracker = tracker

    def return_objects(self, bearingRange=[-30,30], timeRange=[0,5000], rngRange=None):
        """ Returns objects passing within given bearing range of boat in given time range

        Inputs:
            bearingRange -- Angle (in degrees) from bow to search within (0 to 360)
            timeRange -- Time (in ms) to search within using current boat velocity
            rngRange -- Range (in m) from bow to search within 
        
        Returns:
            return_list -- list made up of objects fitting criteria specified
        """
        return self.tracker.return_objects(bearingRange, timeRange, rngRange)

    def get_buoys(self):
        return self.tracker.get_buoys()

    