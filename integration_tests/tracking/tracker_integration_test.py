from threading import Thread

import numpy as np

import matplotlib
matplotlib.use('QT5Agg')

from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

from pubsub import pub
from random import uniform, randint
from time import sleep

import pdb

from src.tracking.map import Map
from src.utils.time_in_millis import time_in_millis

class TrackerTest(Thread):
    """Integration test for tracking system"""
    def __init__(self):
        super().__init__()

        """Initializes tracker test"""
        self.update_interval = 0.5

        # initialize map
        self.map = Map(None, True)

        # create polar plot
        self.fig = plt.figure()
        self.polar = self.fig.add_subplot(111, projection='polar')
        self.polar.set_ylim(0, 100)
        self.polar.grid(True)
        self.polar.set_title('Tracker Map')

        # set up rng, bearing, and type data lists for tracks
        self.track_rng_data = [0]
        self.track_bearing_data = [0]
        self.track_type_data = [0]
        self.tracks = self.polar.scatter(self.track_rng_data, self.track_bearing_data, c='#4444ff', label='Tracks', s=3)
        self.covar_ellipses = []

        # set up rng, bearing, and type data lists for tracks
        self.det_rng_data = [0]
        self.det_bearing_data = [0]
        self.det_type_data = [0]
        self.dets = self.polar.scatter(self.det_rng_data, self.det_bearing_data, c='#ff4444', label='Detections', s=3)

        # set up legend
        box = self.polar.get_position()
        self.polar.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        # Put a legend below current axis
        self.polar.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=5)

        # show plot (and set up blitting)
        plt.show(block=False)
        plt.pause(0.01)
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.polar.bbox)

        # create initial detections
        num_initial_detections = 2
        self.det_pattern_list = ['static', 'circle']
        self.frame_bounds = [(50, 100), (-180, 180)]
        self.spawn_detections(num_initial_detections)

        # start tracker
        self.map.start()

        # initialize old update time (of detection)
        self.prev_time = [time_in_millis()] * num_initial_detections

    def run(self):
        """Continually updates detections"""
        while True:
#            cmd = input()                     # waits for key press to advance
#            if cmd == 's':
#                pdb.set_trace()

            # update detections
            self.update_detections()

            # get tracks from map
            self.get_data()

            # plot tracks and detections on map
            self.plot_data()

            sleep(self.update_interval)

    def update_detections(self):
        """Updates detections by random dr and dtheta"""
        # loop through detections
        for ii in range(len(self.epoch_frame)):
            # generate deltas
            rand_dr = 0 #uniform(-0.01, 0.01)
            rand_dtheta = 0 #uniform(-0.001, 0.001)
            if self.det_pattern_list[ii] == 'circle':
                dr = rand_dr*(time_in_millis() - self.prev_time[ii])/1000
                dtheta = (rand_dtheta + 10)*(time_in_millis() - self.prev_time[ii])/1000            # 10 degree bearing step, ccw
                self.prev_time[ii] = time_in_millis()
            elif self.det_pattern_list[ii] == 'static':
                dr = rand_dr*(time_in_millis() - self.prev_time[ii])/1000
                dtheta = (rand_dtheta)*(time_in_millis() - self.prev_time[ii])/1000

            # update detection with deltas
            self.epoch_frame[ii] = (self.epoch_frame[ii][0] + dr, self.epoch_frame[ii][1] + dtheta, self.epoch_frame[ii][2])

        # set detections for plotting
        self.det_rng_data = [det[0] for det in self.epoch_frame]
        self.det_bearing_data = [det[1] for det in self.epoch_frame]
        self.det_type_data = [det[2] for det in self.epoch_frame]

        # update map with detections
        pub.sendMessage('object(s) detected', epoch_frame = self.epoch_frame, frame_bounds = self.frame_bounds)

        for ii, (det_rng, det_bearing) in enumerate(zip(self.det_rng_data, self.det_bearing_data)):
            print("Detection {}: {}".format(ii, (det_rng, det_bearing)))
            pass

    def spawn_detections(self, n_dets):
        """
        Creates n_dets random detections and places on Map
        Inputs:
            n_dets -- number of detections to create
        Side effects:
            Causes map update
        """
        # initialize epoch frame
        epoch_frame = [0] * n_dets

        # generate random detections
        for ii in range(n_dets):
            rand_rng = uniform(*self.frame_bounds[0])
            rand_bearing = uniform(*self.frame_bounds[1])
            rand_type = randint(0, 2)
            
            # place in epoch_frame
            epoch_frame[ii] = (rand_rng, rand_bearing, rand_type)

        # save off epoch_frame
        self.epoch_frame = epoch_frame

    def get_data(self):
        """Gets data from map return_object function"""
        # get data
        data = self.map.return_objects(bearingRange=[-180, 180], rngRange=[0, 200])

        # split data into rng, bearing, and type_data
        self.track_rng_data = [obj.rng for obj in data]
        self.track_bearing_data = [obj.bearing for obj in data]
        self.track_type_data = [obj.objectType for obj in data]

    def plot_data(self):
        """Updates plot using data"""
        # update tracks data
        self.tracks.set_offsets([*zip(self._deg_2_rad(self.track_bearing_data), self.track_rng_data)])
        self.draw_covar_ellipses(self._deg_2_rad(self.track_bearing_data), self.track_rng_data)

        # update detections data
        self.dets.set_offsets([*zip(self._deg_2_rad(self.det_bearing_data), self.det_rng_data)])

        # restore background (blitting)
        self.fig.canvas.restore_region(self.background)

        # draw tracks and dets
#        self.polar.draw_artist(self.tracks)
        for ellipse in self.covar_ellipses:
            self.polar.draw_artist(ellipse)
        self.polar.draw_artist(self.dets)
        self.fig.canvas.blit(self.polar.bbox)

        self.fig.canvas.flush_events()

        for ii, (track_rng, track_bearing) in enumerate(zip(self.track_rng_data, self.track_bearing_data)):
            print("Track {}: {}".format(ii, (track_rng, track_bearing)))

    def draw_covar_ellipses(self, track_bearing_data, track_rng_data):
        """
        Draws covariance ellipses for each track
        Inputs:
            track_bearing_data -- list of track bearings (in rad)
            track_rng_data -- list of track ranges
        Side Effects:
            self.covar_ellipses -- sets list of covar ellipses to new origin, size
        """
        # remove old ellipses from plot
        for artist in self.covar_ellipses:
            artist.remove()

        # re-init covar_ellipses list
        self.covar_ellipses = [0] * len(track_bearing_data)
        
        # generate ellipses for each track
        # NOTE: current method of getting covariances is a bit of hack... should create API to get covars in future
        for ii, (track_bearing, track_rng) in enumerate(zip(track_bearing_data, track_rng_data)):
            ellipse_center = (track_bearing, track_rng)
            ellipse_rng_radius = self.map.object_list[ii].kalman.covar[0, 0]
            ellipse_bearing_radius = np.radians(self.map.object_list[ii].kalman.covar[1, 1])

            self.covar_ellipses[ii] = Ellipse(ellipse_center, ellipse_bearing_radius, ellipse_rng_radius, \
                                              angle = np.radians(track_bearing), fill = False)

            self.polar.add_artist(self.covar_ellipses[ii])

#            print("Ellipse {}: {}".format(ii, (ellipse_rng_radius, ellipse_bearing_radius)))

    def _deg_2_rad(self, data):
        """Converts degrees to radians for plotting"""
        return [elem * (np.pi)/ 180. for elem in data]
