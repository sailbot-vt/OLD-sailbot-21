from threading import Thread, Lock

from pubsub import pub
from time import sleep
from math import ceil
from statistics import mean
import numpy as np

from src.autonomy.obstacle_avoidance.config_reader import read_object_field_config
from src.autonomy.obstacle_avoidance.config_reader import read_gap_config

mutex_waypoint, mutex_object_field = Lock(), Lock()
class ObstacleAvoidance(Thread):
    """Obstacle avoidance thread"""
    def __init__(self, tracker, boat):
        """
        Initializes obstacle avoidance thread
        Inputs:
            tracker -- tracker instance
            boat -- boat object containing boat state data
        """
        super().__init__()
        self.tracker = tracker
        self.boat = boat

        self.waypoint = (0, 0)                              # range, bearing
        pub.subscribe(self.update_waypoint, 'update waypoint')

        self.is_active = True

        self.object_field_config = read_object_field_config()
        self.gap_config = read_gap_config()

        self.update_interval = 0.5

        self._make_time_bounds()
        self._make_theta_bounds()

        # TODO REMOVE
        self.gap_matrix = np.ones((len(self.t_bounds), len(self.theta_bounds)))

    def run(self):
        """Runs obstacle avoidance thread"""
        while self.is_active:
            # get objects in near field
            self.get_objects()

            # find optimal avoiding path
            adjusted_heading = self.find_path()

            # initiate movement using pubsub
            pub.sendMessage('set heading', adjusted_heading = adjusted_heading)

            sleep(self.update_interval)

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
        # find desired heading
        desired_heading = self.waypoint[1]

        if len(self.object_field) != 0:
            # create gap matrix
            gap_matrix, theta_list = self.create_gap_matrix()

            # find paths without obstacles (assuming constant heading over time range) (constraint probably acceptable given turning rate of boat AND short time ranges for obstacle detection)
            gap_paths = np.sum(gap_matrix, 0).tolist()

            # transform path indices into headings
            poss_paths = [theta for theta, path in zip(theta_list, gap_paths) if path == gap_matrix.shape[0]]

            if len(poss_paths) != 0:            # if any possible path
                # find best path
                delta_list = [abs(theta - desired_heading) for theta in poss_paths]
                adjusted_heading = poss_paths[delta_list.index(min(delta_list))]

                return adjusted_heading

            else:
                return desired_heading

        else:
            return desired_heading
 
    def create_gap_matrix(self):
        """
        Creates gap matrix using object field
        Returns:
            gap_matrix -- matrix with 0's in fields where obstacles are present
            theta_list -- list of bearings corresponding to columns in gap matrix
        """
        # t step
        t_step = self.gap_config['t_step']

        num_predicts = self.object_field_config['num_predictions']

        mutex_object_field.acquire()
        # generate object field with predicted obstacle positions
        predicted_object_field = [(rng + ((ii%(num_predicts+1))*t_step*rng_rate), 
                                    bearing + (ii%(num_predicts+1))*t_step*bearing_rate, obj_type) 
                                  for ii, (rng, bearing, obj_type, rng_rate, bearing_rate) in
                                  enumerate((num_predicts + 1)*self.object_field)]

        # create gap matrix
        gap_matrix = np.ones((len(self.t_bounds),len(self.theta_bounds)))
        for ii, t_bound in enumerate(self.t_bounds):
            # calc range bounds given t_bounds
            rng_bound = tuple(t * self.boat.current_speed() for t in t_bound)
            for jj, theta_bound in enumerate(self.theta_bounds):
                # place 0 in gap matrix IF object exists in bounds
                for obj in predicted_object_field:
                    if rng_bound[0] <= obj[0] <= rng_bound[1] and \
                       theta_bound[0] <= obj[1] <= theta_bound[1]:
                        gap_matrix[ii,jj] = 0

        mutex_object_field.release()

        # generate theta list
        theta_list = [mean(theta_bound) for theta_bound in self.theta_bounds]

        # TODO REMOVE
        self.gap_matrix = gap_matrix    # exposes gap matrix to integration test script

        # return gap matrix
        return gap_matrix, theta_list

    def _make_time_bounds(self):
        """
        Makes time bounds for gap matrix
        Side Effects:
            self.t_bounds -- fills time bounds
        """
        # t step
        t_step = self.gap_config['t_step']

        # get time ranges
        time_range = self.object_field_config['time_range']

        # overlap
        overlap = self.gap_config['overlap']

        # initialize time/range bounds list
        t_bounds = [0] * ceil((abs(time_range[1] - time_range[0])/t_step) * (1-overlap)**(-1))

        # fill out time/range bounds list
        for ii in range(len(t_bounds)):
            l_bound = (ii * (time_range[1] - time_range[0])) / len(t_bounds) + time_range[0]
            r_bound = l_bound + t_step
            if r_bound > time_range[1]:
                r_bound = time_range[1]
            t_bounds[ii] = (l_bound, r_bound)

        self.t_bounds = t_bounds
    
    def _make_theta_bounds(self):
        """
        Makes theta bounds for gap matrix
        Side Effects:
            self.theta_bounds -- fills bearing bounds
        """
        # theta step
        theta_step = self.gap_config['theta_step']

        # get bearing range
        theta_range = self.object_field_config['bearing_range']

        # overlap
        overlap = self.gap_config['overlap']

        # initialize bearing bounds list
        theta_bounds = [0] * ceil((abs(theta_range[1] - theta_range[0])/theta_step) * (1-overlap)**(-1))

        # fill out bearing bounds list
        for jj in range(len(theta_bounds)):
            l_bound = (jj  * (theta_range[1] - theta_range[0])) / len(theta_bounds) + theta_range[0]
            r_bound = l_bound + theta_step
            if r_bound > theta_range[1]:
                r_bound = theta_range[1]
            theta_bounds[jj] = (l_bound, r_bound)

        self.theta_bounds = theta_bounds
