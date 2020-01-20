import numpy as np

import matplotlib
matplotlib.use('QT5Agg')

from matplotlib import pyplot as plt
from matplotlib import animation as ani

from pubsub import pub
from random import uniform, randint
from time import sleep

import pdb

from src.tracking.map import Map

class TrackerTest():
    """Integration test for tracking system"""
    def __init__(self):
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
        self.tracks = self.polar.scatter(self.track_rng_data, self.track_bearing_data, c='#4444ff')

        # set up rng, bearing, and type data lists for tracks
        self.det_rng_data = [0]
        self.det_bearing_data = [0]
        self.det_type_data = [0]
        self.dets = self.polar.scatter(self.det_rng_data, self.det_bearing_data, c='#ff4444')

        # show plot (and set up blitting)
        plt.show(block=False)
        plt.pause(0.01)
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.polar.bbox)

        # create initial detections
        num_initial_detections = 1
        self.frame_bounds = [(0, 100), (-70, 70)]
        self.spawn_detections(num_initial_detections)

    def run(self):
        """Continually updates detections"""
        while True:
            sleep(self.update_interval)
            # get tracks from map
            self.get_data()

            # plot tracks and detections on map (as ranges for tracks TODO)
            self.plot_data()

            # update detections
            self.update_detections()

    def update_detections(self):
        """Updates detections by random dr and dtheta"""
        # loop through detections
        for ii in range(len(self.epoch_frame)):
            # generate deltas
            dr = uniform(-1, 1)
            dtheta = uniform(-1, 1)
            # update detection with deltas
            self.epoch_frame[ii] = (self.epoch_frame[ii][0] + dr, self.epoch_frame[ii][1] + dtheta, self.epoch_frame[ii][2])

        # set detections for plotting
        self.det_rng_data = [det[0] for det in self.epoch_frame]
        self.det_bearing_data = [det[1] for det in self.epoch_frame]
        self.det_type_data = [det[2] for det in self.epoch_frame]

        # update map with detections
        pub.sendMessage('object(s) detected', epoch_frame = self.epoch_frame, frame_bounds = self.frame_bounds)

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

        # send object detections to map
        pub.sendMessage('object(s) detected', epoch_frame = epoch_frame, frame_bounds = self.frame_bounds)

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
        self.tracks.set_offsets([self._deg_2_rad(self.track_bearing_data), self.track_rng_data])

        # update detections data
        self.dets.set_offsets([self._deg_2_rad(self.det_bearing_data), self.det_rng_data])

        # restore background (blitting)
        self.fig.canvas.restore_region(self.background)

        # draw tracks and dets
        self.polar.draw_artist(self.tracks)
        self.polar.draw_artist(self.dets)
        self.fig.canvas.blit(self.polar.bbox)

        self.fig.canvas.flush_events()

        print(*zip(self.track_rng_data, self.track_bearing_data))

    def _deg_2_rad(self, data):
        """Converts degrees to radians for plotting"""
        return [elem * (np.pi)/ 180. for elem in data]
