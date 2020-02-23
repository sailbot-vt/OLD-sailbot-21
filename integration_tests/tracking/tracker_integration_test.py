from threading import Thread

import numpy as np

import matplotlib
matplotlib.use('QT5Agg')

from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

from pubsub import pub
from random import uniform, randint
from time import sleep

from src.tracking.map import Map
from src.utils.time_in_millis import time_in_millis

class TrackerTest(Thread):
    """Integration test for tracking system"""
    def __init__(self):
        super().__init__()

        """Initializes tracker test"""
        self.update_interval = 0.25

        # initialize map
        self.map = Map(None, True)

        # create polar plot
        self.fig = plt.figure()
        self.polar = self.fig.add_subplot(111, projection='polar')
        self.polar.set_ylim(0, 200)
        self.polar.grid(True)
        self.polar.set_title('Tracker Map')

        # set up rng, bearing, and type data lists for tracks
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

        # color plot grey
        self.polar.set_facecolor('#F5F5F5')
        self.polar.set_alpha(0.2)

        # show plot (and set up blitting)
        plt.show(block=False)
        plt.pause(0.01)
        self.fig.canvas.draw()

        input('Make plot full screen then press enter')
        self.background = self.fig.canvas.copy_from_bbox(self.polar.bbox)

        # create initial detections
        num_initial_detections = 18
        # patterns: static, circle_CCW, circle_CW, circle_CCW_radial_out, circle_CW_radial_out, radial_out
        self.rng_rate_list = [0, 0, 0, 0.05, 0.05, 0.075] * 3
        self.bearing_rate_list = [0, 0.0375, -0.0375, 0.025, -0.025, 0] * 3
        self.frame_bounds = [(10, 175), (-180, 180)]
        self.spawn_detections(num_initial_detections)

        # set look frame parameters
        self.look_frame = 'aperture'     #'full'
        self.look_rng = (0, 150)        # initial (and perm) range range of look aperture
        self.look_bearing = (-70, 70)   # initial bearing range of look aperture
        self.look_sweep = (-30, 30)     # sweeps so that the center of the aperture goes between these two points
        self.pan_direction = 1          # direction of pan (+1 = CW, -1 = CCW)
        self.look_apertures = []
        self.num_apertures = 1

        # detection parameters
        self.detect_mode = 'regular' #'constant' #'random'
        self.detect_probability = 0.6

        # start tracker
        self.map.start()

        # initialize old update time (of detection)
        self.prev_time = [time_in_millis()] * num_initial_detections

    def run(self):
        """Continually updates detections"""
        loop_counter = 0
        while True:
            sleep(self.update_interval)

            # get tracks from map
            self.get_data()

            # plot tracks and detections on map
            self.plot_data()

            # update detections
            self.update_detections(loop_counter)

            if self.look_frame == 'aperture':
                # move aperture
                self.pan_aperture()

            loop_counter = (loop_counter + 1) % 4

    def update_detections(self, send_counter):
        """Updates detections by random dr and dtheta"""
        # loop through detections
        for ii in range(len(self.epoch_frame)):
            # get dt
            dt = (time_in_millis() - self.prev_time[ii]) / 1000.
            # get rng and bearing rate
            rng_rate, bearing_rate = self.rng_rate_list[ii], self.bearing_rate_list[ii]

            # adjust bearing rate based on distance from origin
            bearing_rate /= 0.5* self.epoch_frame[ii][0]

            # generate deltas
            rand_dr = uniform(-0.01, 0.01)
            rand_dtheta = uniform(-0.001, 0.001)
            
            dr = (rand_dr + rng_rate) * dt
            dtheta = (rand_dtheta + bearing_rate) * dt

            # fix wraparound
            theta = self.epoch_frame[ii][1] + dtheta
            rng = self.epoch_frame[ii][0] + dr
            if theta > 180:
                theta = -180 + (theta % 180)

            if rng < 0:
                rng *= -1
                theta %= -180

            # update detection with deltas
            self.epoch_frame[ii] = (rng, theta, self.epoch_frame[ii][2])

        # set detections for plotting
        self.det_rng_data = [det[0] for det in self.epoch_frame]
        self.det_bearing_data = [det[1] for det in self.epoch_frame]
        self.det_type_data = [det[2] for det in self.epoch_frame]

        idx_list = [1] * len(self.epoch_frame)

        if self.look_frame == 'aperture':
            # trim epoch frame to objects in view look aperture
            for ii, obj in enumerate(self.epoch_frame):
                if not self.look_rng[0] <= obj[0] <= self.look_rng[1] or \
                   not self.look_bearing[0] <= obj[1] <= self.look_bearing[1]:
                    idx_list[ii] = 0

        if self.detect_mode == 'random':
            # trim epoch frame using randint (to determine whether or not to send data)
            for ii in range(len(idx_list)):
                if randint(0, 9) >= (self.detect_probability * 10):
                    idx_list[ii] = 0

        elif self.detect_mode == 'regular':
            if send_counter != 0:
                idx_list = [0] * len(idx_list)

        elif self.detect_mode == 'constant':
            pass

        epoch_frame = [obj for (ii, obj) in zip(idx_list, self.epoch_frame) if ii == 1 ]

        # update map with detections
        pub.sendMessage('object(s) detected', epoch_frame = epoch_frame, frame_bounds = self.frame_bounds)

    def spawn_detections(self, n_dets):
        """
        Creates n_dets random detections and places on Map
        Inputs:
            n_dets -- number of detections to create
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
        self.track_rng_data = [obj[0] for obj in data]
        self.track_bearing_data = [obj[1] for obj in data]
        self.track_type_data = [obj[2] for obj in data]
        self.track_conf_data = [obj[5] for obj in data]

    def plot_data(self):
        """Updates plot using data"""
        # update tracks data
        self.draw_covar_ellipses(self._deg_2_rad(self.track_bearing_data), self.track_rng_data, self.track_conf_data)

        # update look aperture
        self.draw_look_aperture()

        # update detections data
        self.dets.set_offsets([*zip(self._deg_2_rad(self.det_bearing_data), self.det_rng_data)])

        # restore background (blitting)
        self.fig.canvas.restore_region(self.background)

        # draw tracks and dets
        for ellipse in self.covar_ellipses:
            self.polar.draw_artist(ellipse)
        self.polar.draw_artist(self.dets)

        # draw look aperture
        for line in self.look_apertures:
            self.polar.draw_artist(line[0])

        self.fig.canvas.blit(self.polar.bbox)

        self.fig.canvas.flush_events()

        for ii, track_conf in enumerate(self.track_conf_data):
            print("Track {}: confidence -- {}".format(ii, track_conf))
        print("Track List Length: {}".format(len(self.track_conf_data)))
        print('-------------------------------------------------------')

    def pan_aperture(self):
        """
        Pans look aperture
        Side effects:
            self.look_bearing -- pans look bearing (at 0.5 deg per step)
        """
        bearing_rate = 0.5
        aperture_center = sum(self.look_bearing) / 2.
        new_ap_center = aperture_center + (bearing_rate * self.pan_direction)

        if new_ap_center > self.look_sweep[1]:
            new_ap_center = self.look_sweep[1] - (new_ap_center % self.look_sweep[1])
            self.pan_direction *= -1
        elif new_ap_center < self.look_sweep[0]:
            new_ap_center = self.look_sweep[0] - (new_ap_center % self.look_sweep[0])
            self.pan_direction *= -1

        diff = new_ap_center - aperture_center
        self.look_bearing = tuple(bear + diff for bear in self.look_bearing[:])

    def draw_look_aperture(self):
        """
        Draws look aperture
        Side Effects:
            self.look_apertures -- changes look aperture to reflect new look direction
        """
        # remove old aperture from plot
        for artist in self.look_apertures:
            self.polar.lines.remove(artist[0])

        # re-init look_apertures list
        self.look_apertures = [0] * 3

        # create wedge
        rad_look_bearing = self._deg_2_rad(self.look_bearing)
        self.look_apertures[0] = self.polar.plot([rad_look_bearing[0]] * 2, [self.look_rng[0], self.look_rng[1]], \
                                                  '--', color = 'g', alpha = 0.6)
        self.look_apertures[1] = self.polar.plot([rad_look_bearing[1]] * 2, [self.look_rng[0], self.look_rng[1]], \
                                                  '--', color = 'g', alpha = 0.6)
        bearing_sweep = np.arange(rad_look_bearing[0], rad_look_bearing[1], (rad_look_bearing[1] - rad_look_bearing[0]) / 100.)
        self.look_apertures[2] = self.polar.plot(bearing_sweep, [self.look_rng[1]] * 100, \
                                                  '--', color = 'g', alpha = 0.6)

        for aperture in self.look_apertures:
            self.polar.add_artist(aperture[0])

    def draw_covar_ellipses(self, track_bearing_data, track_rng_data, track_conf_data):
        """
        Draws covariance ellipses for each track
        Inputs:
            track_bearing_data -- list of track bearings (in rad)
            track_rng_data -- list of track ranges
            track_conf_data -- list of track confidences
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
        for ii, (track_bearing, track_rng, track_conf) in enumerate(zip(track_bearing_data, track_rng_data, track_conf_data)):
            ellipse_center = (track_bearing, track_rng)
            ellipse_rng_radius = self.map.object_list[ii].kalman.covar[0, 0]
            ellipse_bearing_radius = np.radians(self.map.object_list[ii].kalman.covar[1, 1])
            ellipse_conf = track_conf
            if ellipse_conf > 0.7:
                color = 'green'
            elif ellipse_conf > 0.3:
                color = 'blue'
            else:
                color = 'red'

            alpha = 0.4

            self.covar_ellipses[ii] = Ellipse(ellipse_center, ellipse_bearing_radius, ellipse_rng_radius, \
                                              angle = np.radians(track_bearing), alpha = alpha, color = color)

            self.polar.add_artist(self.covar_ellipses[ii])

#            print("Ellipse {}: {}".format(ii, (ellipse_rng_radius, ellipse_bearing_radius)))

    def _deg_2_rad(self, data):
        """Converts degrees to radians for plotting"""
        return [elem * (np.pi)/ 180. for elem in data]
