from threading import Thread, Lock

from pubsub import pub
from math import ceil

from src.autonomy.obstacle_avoidance.config_reader import read_object_field_config
from src.autonomy.obstacle_avoidance.config_reader import read_gap_config

mutex_waypoint, mutex_object_field = Lock(), Lock()
class ObstacleAvoidance(Thread):
    """Obstacle avoidance thread"""
    def __init__(self, wind, tracker, boat):
        """
        Initializes obstacle avoidance thread
        Inputs:
            wind -- wind object containing true and apparent wind reading
            tracker -- tracker instance
            boat -- boat object containing boat state data
        """
        super().__init__()
        self.wind = wind
        self.tracker = tracker
        self.boat = boat

        self.waypoint = (0, 0)
        pub.subscribe(self.update_waypoint, 'waypoint')

        self.is_active = True

        self.object_field_config = read_object_field_config()
        self.gap_config = read_gap_config()

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
        # create gap matrix
        gap_matrix = self.create_gap_matrix()
        
    def create_gap_matrix(self):
        """
        Creates gap matrix using object field
        Returns:
            gap_matrix -- matrix with 0's in fields where obstacles are present
        """
        # t and theta steps
        t_step = self.gap_config['t_step']
        theta_step = self.gap_config['theta_step']

        # overlap
        overlap = self.gap_config['overlap']
        
        # initialize time/range bounds list
        t_bounds = [0] * ceil((abs(time_range[1] - time_range[0])/t_step) * (1-overlap)^-1)
        # initialize bearing bounds list
        theta_bounds = [0] * ceil((abs(theta_range[1] - theta_range[0])/theta_step) * (1-overlap)^-1)

        # fill out time/range bounds list
        for ii in range(len(t_bounds)):
            l_bound = (ii * (time_range[1] - time_range[0])) / len(t_bounds) - mean(time_range)
            r_bound = l_bound + t_step
            t_bounds[ii] = (l_bound, r_bound)

        # fill out bearing bounds list
        for jj in range(len(theta_bounds)):
            l_bound = (jj * (theta_range[1] - theta_range[0])) / len(theta_bounds) - mean(theta_range)
            r_bound = l_bound + theta_step
            theta_bounds[jj] = (l_bound, r_bound)

        # create gap matrix
        gap_matrix = np.ones((len(t_bounds),len(theta_bounds)))
        mutex_object_field.acquire()
        for ii, t_bound in enumerate(t_bounds):
            # calc range bounds given t_bounds
            rng_bound = (t * self.boat.current_speed() for t in t_bound)
            for jj, theta_bound in enumerate(theta_bounds):
                # place 0 in gap matrix IF object exists in bounds
                for obj in self.object_field:
                    if rng_bound[0] <= obj[0] <= rng_bound[1] and \
                       theta_bound[0] <= obj[1] <= theta_bound[1]:
                        gap_matrix[ii,jj] = 0
                        break

        mutex_object_field.release()

        # return gap matrix
        return gap_matrix
