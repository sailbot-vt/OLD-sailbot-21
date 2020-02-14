from threading import Thread, Lock

from src.autonomy.obstacle_detection import read_object_field_config

mutex = Lock()
class ObstacleAvoidance(Thread):
    """Obstacle avoidance thread"""
    def __init__(self, wind, tracker):
        """
        Initializes obstacle avoidance thread
        Inputs:
            wind -- wind object containing true and apparent wind reading
            tracker -- tracker instance
        """
        self.wind = wind
        self.tracker = tracker

        self.waypoint = (0, 0)
        pub.subscribe('waypoint', self.update_waypoint)

        self.is_active = True

        self.object_field_config = read_object_field_config()

    def run(self):
        """Runs obstacle avoidance thread"""
        while self.is_active:
            # get objects in near field
            # find optimal avoiding path
            # initiate movement using pubsub
            pass

    def update_waypoint(self, new_waypoint):
        """
        Updates objective waypoint
        Inputs:
            new_waypoint -- tuple containing rng and bearing of new waypoint
        Side Effects:
            self.waypoint -- updates self.waypoint
        """
        mutex.acquire()
        self.waypoint = new_waypoint
        mutex.release()

    def quit(self):
        """Quits obstacle avoidance thread"""
        self.is_active = False

    def get_objects(self):
        """
        Gets list of objects
        Side effects:
            self.object_field -- sets object field using return_objects method from map
        """
        time_range = self.object_field_config['time_range']
        bearing_range = self.object_field_config['bearing_range']

        object_list = self.tracker.return_objects(bearingRange = bearing_range, timeRange = time_range)

        mutex.acquire()
        self.object_field = [(obj.rng, obj.bearing, obj.objectType) for obj in object_list]
        mutex.release()
