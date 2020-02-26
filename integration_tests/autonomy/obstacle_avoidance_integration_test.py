import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from threading import Thread

import numpy as np
from math import ceil

import matplotlib
matplotlib.use('QT5Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Arrow

from pubsub import pub
from random import uniform, randint
from time import sleep

from src.autonomy.obstacle_avoidance.obstacle_avoidance import ObstacleAvoidance
from src.utils.time_in_millis import time_in_millis

class ObstacleAvoidanceTest(Thread):
    """Integration test for obstacle avoidance system"""
    def __init__(self):
        """Initializes obstacle avoidance test"""
        super().__init__()

        self.update_interval = 0.1

        # set up mock tracker
        self.tracker = MagicMock(name='map')
        self.tracker.return_objects.return_value = []

        # set up mock boat and set boat movement parameters
        self.boat = MagicMock(name='boat')
        self.boat_speed = 0.5   # m/s
        self.boat_bearing_rate = 5        # deg/s
        self.rel_heading = 0
        self.boat.current_speed.return_value = self.boat_speed

        # initialize obstacle avoidance thread
        self.obstacle_avoidance = ObstacleAvoidance(self.tracker, self.boat)

        # create polar plot
        self.fig = plt.figure()
        self.polar = self.fig.add_subplot(111, projection='polar')
        self.plot_rng_range = (0, 18)
        self.polar.set_ylim(self.plot_rng_range[0], self.plot_rng_range[1])
        self.plot_bearing_range = (-45, 45)
        self.polar.set_thetamin(self.plot_bearing_range[0])
        self.polar.set_thetamax(self.plot_bearing_range[1])
        self.polar.grid(True)
        self.polar.set_title('Obstacle Avoidance Map')

        # color plot grey
        self.polar.set_facecolor('#F5F5F5')
        self.polar.set_alpha(0.2)

        # set up boat arrow
        self.boat_arrow = None

        # set up obstacle avoidance area visualization
        self.bearing_range = self.obstacle_avoidance.object_field_config['bearing_range']
        rad_bearing_range = self._deg_2_rad(self.bearing_range)
        self.rng_range = [time * self.boat_speed for time in self.obstacle_avoidance.object_field_config['time_range']]
        self.polar.plot([rad_bearing_range[0]] *2, [self.rng_range[0], self.rng_range[1]], \
                        '--', color='g', alpha=0.6)
        self.polar.plot([rad_bearing_range[1]] *2, [self.rng_range[0], self.rng_range[1]], \
                        '--', color='g', alpha=0.6)
        bearing_sweep = np.arange(rad_bearing_range[0], rad_bearing_range[1], (rad_bearing_range[1]-rad_bearing_range[0]) / 50.)
        self.polar.plot(bearing_sweep, [self.rng_range[1]] * 50, \
                        '--', color='g', alpha=0.6, label='Obstacle Avoidance Area')

        # set up obstacle scatter plot
        self.obstacle_rng_data = [0]
        self.obstacle_bearing_data = [0]
        self.obstacles = self.polar.scatter(self.obstacle_rng_data, self.obstacle_bearing_data, c='#ff4444', \
                                            label='Obstacles', s=3)

        # set up legend
        box = self.polar.get_position()
        self.polar.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        # Put a legend below current axis
        self.polar.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=5)

        # create imshow plot
        self.sector_fig = plt.figure()
        self.sectorview_ax = self.sector_fig.add_subplot(111)
        self.sectorview = self.sectorview_ax.imshow(np.ones((len(self.rng_range), len(self.bearing_range))), \
                                                      extent=[*self.bearing_range, *self.rng_range], cmap = 'plasma')
        self.sectorview_ax.set_title('Sector View')
        self.sectorview_ax.set_xlabel('Bearing')
        self.sectorview_ax.set_ylabel('Range')

        # show plot (and set up blitting)
        plt.show(block=False)
        plt.pause(0.01)
        self.fig.canvas.draw()
        self.sector_fig.canvas.draw()

        input('Make plot full screen then press enter')
        self.background = self.fig.canvas.copy_from_bbox(self.polar.bbox)
        self.sector_background = self.sector_fig.canvas.copy_from_bbox(self.sectorview_ax.bbox)

        # spawn obstacles
        self.num_obstacles = 64
        self.obstacle_rng_rates = [0, 0, 0, 0, 0.2, -0.2, 0.1, 0] * 8
        self.obstacle_bearing_rates = [0, 0, 0, 0, 0, 0, -0.3, 0.2] * 8
        self.spawn_obstacles()

        # subscribe to set heading
        pub.subscribe(self.update_heading, 'set heading')

        # start obstacle avoidance thread
        self.obstacle_avoidance.start()

    def run(self):
        """Run loop for obstacle avoidance test"""
        while 1:
            # update obstacles
            self.update_obstacles()

            # plot data
            self.plot_data()

            sleep(self.update_interval)

    def spawn_obstacles(self):
        """
        Spawns obstacles (initial position is randomly placed in plot area)
        Side Effects:
            self.obstacle_rng_data -- range data for obstacles
            self.obstacle_bearing_data -- bearing data for obstacles
        """

        # spawn random obstacles in field bounds and set obstacle data (for plotting)
        self.obstacle_rng_data = [self.plot_rng_range[1] for _ in range(self.num_obstacles)]
        self.obstacle_bearing_data = [uniform(*self.plot_bearing_range) for _ in range(self.num_obstacles)]

    def update_obstacles(self):
        """Updates obstacle positions (using mocked boat movement, obstacle movement)"""
        # init object field
        object_field = [0] * self.num_obstacles

        for ii, (obstacle_rng, obstacle_bearing, rng_rate, bearing_rate) in \
            enumerate(zip(self.obstacle_rng_data, self.obstacle_bearing_data, 

                          self.obstacle_rng_rates, self.obstacle_bearing_rates)):
            # account for ownship movement
            ownship_dr, ownship_dtheta = self._ownship_delta(obstacle_rng, obstacle_bearing, \
                                                             self.boat_speed, self.rel_heading)

            # apply obstacle movement
            dr = (rng_rate * self.update_interval) + ownship_dr
            dtheta = (bearing_rate * self.update_interval) + ownship_dtheta

            new_r = obstacle_rng + dr
            new_theta = obstacle_bearing + dtheta

            # trim obstacles that went past boat
            if (-45 <= new_theta <= 45):
                object_field[ii] = (new_r, new_theta, 0, \
                                    dr/self.update_interval, dtheta/self.update_interval)
            else:
                # spawn a new detection
                object_field[ii] = (self.plot_rng_range[1], uniform(*self.plot_bearing_range), 0, 0, 0)
                print("spawning new detection")

        # trim object field to objects in bounds of obstacle avoidance
        return_object_field = [(rng, bearing, obj_type, rng_rate, bearing_rate)
                               for rng, bearing, obj_type, rng_rate, bearing_rate in object_field
                               if (self.rng_range[0] <= rng <= self.rng_range[1] and
                                   self.bearing_range[0] <= bearing <= self.bearing_range[1])]

        # set return objects mock
        self.tracker.return_objects.return_value = return_object_field

        # set obstacle data (for plotting)
        self.obstacle_rng_data = [rng for rng, _, _, _, _ in object_field]
        self.obstacle_bearing_data = [bearing for _, bearing, _, _, _ in object_field]

    def update_heading(self, heading):
        """Updates heading from obstacle avoidance"""
        self.desired_rel_heading = heading
        print("setting course towards {}".format(heading))

        self.rel_heading += np.sign(heading - self.rel_heading) * (self.boat_bearing_rate * self.update_interval)
        print("new rel heading {}".format(self.rel_heading))

    def plot_data(self):
        """Plots obstacle data, boat heading"""
        # restore background
        self.fig.canvas.restore_region(self.background)
        self.sector_fig.canvas.restore_region(self.sector_background)

        # plot boat movement arrow
        if self.boat_arrow:
            self.boat_arrow.remove()
        self.boat_arrow = Arrow(0, 0, np.radians(self.rel_heading), 10 * self.boat_speed,
                                width=0.5, color='blue', alpha=0.2)
        self.polar.add_artist(self.boat_arrow)
        self.polar.draw_artist(self.boat_arrow)

        # update obstacles
        self.obstacles.set_offsets([*zip(self._deg_2_rad(self.obstacle_bearing_data), self.obstacle_rng_data)])
        self.polar.draw_artist(self.obstacles)

        self.fig.canvas.blit(self.polar.bbox)
        self.fig.canvas.flush_events()

        # update sector plot
        self.sectorview.set_data(np.flipud(self.obstacle_avoidance.gap_matrix))
        self.sectorview_ax.add_artist(self.sectorview)
        self.sectorview_ax.draw_artist(self.sectorview)
        self.sectorview.autoscale()

        self.sector_fig.canvas.blit(self.sectorview_ax.bbox)
        self.sector_fig.canvas.flush_events()

    def _deg_2_rad(self, data):
        """Converts degrees to radians for plotting"""
        return [elem * (np.pi)/ 180. for elem in data]

    def _ownship_delta(self, r, bearing, speed, heading):
        """Returns delta of obstacle coords given ownship speed and heading"""
        prev_x = r * np.cos(np.radians(bearing))
        prev_y = r * np.sin(np.radians(bearing))

        dx = -1 * speed * np.cos(np.radians(heading)) * self.update_interval
        dy = -1 * speed * np.sin(np.radians(heading)) * self.update_interval

        new_x = prev_x + dx
        new_y = prev_y + dy

        new_r = np.sqrt(new_x**2 + new_y**2)
        new_theta = np.arctan2(new_y, new_x)

        return new_r - r, np.degrees(new_theta - np.radians(bearing))
