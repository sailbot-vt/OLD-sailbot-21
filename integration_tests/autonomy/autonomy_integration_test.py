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
from random import randint
from time import sleep

from src.utils.vec import Vec2
from src.utils.time_in_millis import time_in_millis

from src.world.wind import Wind

from src.autonomy.events.fleet_race import FleetRace
"""
from src.autonomy.events.collision_avoidance_event import CollisionAvoidanceEvent
from src.autonomy.events.endurance_race_event import EnduranceRace
from src.autonomy.events.payload_event import PayloadEvent
from src.autonomy.events.precision_navigation_event import PrecisionNavigationEvent
from src.autonomy.events.search_event import SearchEvent
from src.autonomy.events.station_keeping_event import StationKeepingEvent
"""

class AutonomyTest(Thread):
    """Integration test for autonomy system"""
    def __init__(self):
        """Initializes autonomy test"""
        super().__init__()

        self.update_interval = 0.25

        # set up mock tracker
        self.tracker = MagicMock(name='map')
        self.tracker.get_buoys.return_value = []

        # set up mock boat and set boat movement parameters
        self.boat = MagicMock(name='boat')
        self.boat_speed = 1.5   # m/s
        self.boat_bearing_rate = 5        # deg/s
        self.boat.current_heading = 0
        self.boat.upwind_angle = 35
        self.boat.current_speed.return_value = self.boat_speed

        # set up wind
        self.wind = Wind()
        self.wind.update_true_wind_angle(90)        # due North wind

        # initialize event thread
        event = 0

        if event == 0:
            self.event = FleetRace(self.tracker, self.boat, self.wind)    # run fleet race
        elif event == 1:
            self.event = EnduranceRace(self.tracker, self.boat, self.wind) # run endurance race
        elif event == 2:
            self.event = PayloadEvent(self.tracker, self.boat, self.wind)        # run payload event
        elif event == 3:
            self.event = PrecisionNavigationEvent(self.tracker, self.boat, self.wind)        # run precision navigation 
        elif event == 4:
            self.event = StationKeepingEvent(self.tracker, self.boat, self.wind)        # run station keeping
        elif event == 5:
            self.event = CollisionAvoidanceEvent(self.self.tracker, self.boat, self.wind)    # run collision avoidance
        elif event == 6:
            self.event = SearchEvent(self.tracker, self.boat, self.wind)            # run search

        # create polar plot
        self.fig = plt.figure()
        self.polar = self.fig.add_subplot(111, projection='polar')
        self.plot_rng_range = (0, 150)
        self.polar.set_ylim(self.plot_rng_range[0], self.plot_rng_range[1])
        self.polar.grid(True)
        self.polar.set_title('Dynamic Course Map')

        # color plot grey
        self.polar.set_facecolor('#F5F5F5')
        self.polar.set_alpha(0.2)

        # set up boat arrow
        self.boat_arrow = None

        # set up buoy scatter plot
        self.buoy_rng_data = [0]
        self.buoy_bearing_data = [0]
        self.buoys = self.polar.scatter(self.buoy_bearing_data, self.buoy_rng_data, c='#ffa500', \
                                            label='Buoys', s=5)

        # set up waypoint data
        self.waypoint_rng_data = [0]
        self.waypoint_bearing_data = [0]
#        self.waypoints = self.polar.scatter(self.waypoint_bearing_data, self.waypoint_rng_data, c='#00ff00', \
#                                            label='Waypoints', s=4)

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

        input('Make plot full screen then press enter')
        self.background = self.fig.canvas.copy_from_bbox(self.polar.bbox)

        # spawn buoys
        self.spawn_buoys(event)

        # subscribe to set rudder
        self.last_updated = time_in_millis()
        self.prev_heading = 0
        pub.subscribe(self.update_heading, 'set rudder')

    def run(self):
        """Run loop for autonomy test"""
        while 1:
            # update buoys
            self.update_buoys()

            # get waypoints
            self.get_waypoints()

            # plot data
            self.plot_data()

            sleep(self.update_interval)

    def spawn_buoys(self, event):
        """
        Spawns buoys (initial position is randomly placed in plot area)
        Inputs:
            event -- event number
        Side Effects:
            self.buoy_rng_data -- range data for buoys
            self.buoy_bearing_data -- bearing data for buoys
        """
        x_shift = randint(5, 30)
        y_shift = randint(30, 50)
        if event == 0:      # fleet race
            self.num_buoys = 4
            self.buoy_rng_data = [0] * self.num_buoys
            self.buoy_bearing_data = [0] * self.num_buoys

            # create start gate
            self.buoy_rng_data[0], self.buoy_bearing_data[0] = self._cart_2_polar(2.5+x_shift, 0+y_shift)
            self.buoy_rng_data[1], self.buoy_bearing_data[1] = self._cart_2_polar(-2.5+x_shift, 0+y_shift)

            # create buoys to round
            self.buoy_rng_data[2], self.buoy_bearing_data[2] = self._cart_2_polar(15+x_shift, 60+y_shift)
            self.buoy_rng_data[3], self.buoy_bearing_data[3] = self._cart_2_polar(-15+x_shift, 60+y_shift)

    def update_buoys(self):
        """Updates buoy positions (using mocked boat movement)"""
        # init object field
        object_field = [0] * self.num_buoys

        # account for ownship rotation
        rotate_dtheta = self.prev_heading - self.boat.current_heading

        for ii, (buoy_rng, buoy_bearing) in \
            enumerate(zip(self.buoy_rng_data, self.buoy_bearing_data)):
            # account for ownship movement
            ownship_dr, ownship_dtheta = self._ownship_delta(buoy_rng, buoy_bearing, \
                                                             self.boat_speed, self.boat.current_heading)

            new_r = buoy_rng + ownship_dr
            new_theta = buoy_bearing + ownship_dtheta + rotate_dtheta

            object_field[ii] = (new_r, new_theta)

        # set return objects mock
        self.tracker.get_buoys.return_value = object_field

        # set buoy data (for plotting)
        self.buoy_rng_data = [rng for rng, _,  in object_field]
        self.buoy_bearing_data = [bearing for _, bearing in object_field]

    def update_heading(self, degrees_starboard):
        """Updates heading from obstacle avoidance"""
        updated = time_in_millis()
        self.prev_heading = self.boat.current_heading
        self.boat.current_heading += (degrees_starboard / 15.) \
                                     * (self.boat_bearing_rate * (updated - self.last_updated)/1000.)
        print("new rel heading {}".format(self.boat.current_heading))
        self.last_updated = updated

    def get_waypoints(self):
        """Gets waypoints from captain"""
        marks = self.event.captain.path.marks.copy()

        self.waypoint_rng_data = [rng for rng, _ in marks]
        self.waypoint_bearing_data = [bearing for _, bearing in marks]

    def plot_data(self):
        """Plots buoy data, boat heading"""
        # restore background
        self.fig.canvas.restore_region(self.background)

        # plot boat movement arrow
        if self.boat_arrow:
            self.boat_arrow.remove()
        self.boat_arrow = Arrow(0, 0, np.radians(self.boat.current_heading), 50 * self.boat_speed,
                                width=0.5, color='blue', alpha=0.5)
        self.polar.add_artist(self.boat_arrow)
        self.polar.draw_artist(self.boat_arrow)

        # update buoys
        self.buoys.set_offsets([*zip(self._deg_2_rad(self.buoy_bearing_data), self.buoy_rng_data)])
        self.polar.draw_artist(self.buoys)

        # update waypoints
#        self.waypoints.set_offsets([*zip(self._deg_2_rad(self.waypoint_bearing_data), self.waypoint_rng_data)])
        if len(self.waypoint_rng_data) > 0:
#            self.polar.draw_artist(self.waypoints)
            for ii, (bearing, rng) in enumerate(zip(self._deg_2_rad(self.waypoint_bearing_data), self.waypoint_rng_data)):
                annotation = self.polar.annotate(str(ii), xy=(bearing, rng), size=6, \
                                                 textcoords='offset points', xytext=(-0.05, -0.05), \
                                                 ha='center', va='center')
                self.polar.draw_artist(annotation)

        self.fig.canvas.blit(self.polar.bbox)
        self.fig.canvas.flush_events()

    def _deg_2_rad(self, data):
        """Converts degrees to radians for plotting"""
        return [elem * (np.pi)/ 180. for elem in data]

    def _cart_2_polar(self, x, y):
        """Converts from cartesian to polar coords"""
        return (np.sqrt(x**2 + y**2),
                np.arctan2(y, x) * 180/np.pi)

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
