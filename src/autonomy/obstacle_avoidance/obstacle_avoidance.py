from threading import Thread, Lock

from src.autonomy.obstacle_avoidance import read_object_field_config

mutex_waypoint, mutex_object_field = Lock(), Lock()
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
            self.get_objects()
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
        mutex_waypoint.acquire()
        self.waypoint = new_waypoint
        mutex_waypoint.release()

    def quit(self):
        """Quits obstacle avoidance thread"""
        self.is_active = False

    def get_objects(self):
        """
        Gets list of objects
        Side effects:
            self.object_field -- sets object field using return_objects method from map
        """
        # get time and bearing ranges
        time_range = self.object_field_config['time_range']
        bearing_range = self.object_field_config['bearing_range']

        # update object field
        mutex_object_field.acquire()
        self.object_field = self.tracker.return_objects(bearingRange = bearing_range, timeRange = time_range) 
        mutex_object_field.release()

    def find_path(self):
        """
        Finds optimal obstacle avoidance path given desired heading and object field
        Returns:
            adjusted_heading -- heading adjusted for obstacles in near field
        """
        # create gap vector
        
