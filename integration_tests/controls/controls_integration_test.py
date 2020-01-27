# -------------------------------------------------------------------------------------------------------------
# Controls Integration Test Goals:
#   -- design a modular system of testing controls integration (utilizing both software AND hardware tools)
#   -- enable HITL (hardware-in-the-loop) testing using hardware feedback from motors, servos, etc.
#   -- create system in a way that allows for ease of verifiability on multiple levels:
#       -- verify by comparing log files to commands issued
#       -- verify by comparing positional feedback to commands issued
#       -- verify by comparing servo/motor position (visually) to commands issued (and real-time plot created)
#
# Future extensions:
#   -- extend with jib, rear foil, and sensor module
# NOTE:
#   -- since this program requires the use of the adafruit_bbio library to communicate with the arduino, this MUST be run on the #      Beaglebone Black
#   -- connect to the Beaglebone using x11 forwarding ('ssh -Y ...') to show plots on host machine
# -------------------------------------------------------------------------------------------------------------
from time import sleep

import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

from src.sail.sail_listener import SailListener
from src.rudder.rudder_listener import RudderListener
from src.arduino.arduino import Arduino

from integration_tests.controls.test_scheme_enum import TestScheme
from integration_tests.controls.config_reader import read_test_config

class ControlsTest(Thread):
    """Class that performs integration testing for the controls stack (software AND hardware)"""
    def __init__(self):
        """Initializes controls test class"""
        super().__init__()

        # initialize sail listener and rudder listener
        self.sail_listener = SailListener()
        self.rudder_listener = RudderListener()

        # initialize arduino
        self.arduino = Arduino()

        # complete handshake with arduino
        # TODO

        # toggle test scheme
        self.test_scheme = TestScheme.ROTATE

        # read test scheme parameters
        self.test_config = read_test_config(self.test_scheme)
        self.sail_dir = self.test_config['sail']['dir']
        self.rudder_dir = self.test_config['rudder']['dir']
        self.update_interval = self.test_config['update_interval']

        # set initial position
        self.set_positions()

        # set up plots
        self.sail_fig = plt.figure()
        self.sail_plt = self.sail_fig.add_subplot(111, projection='polar')
        self.sail_plt.set_title('Sail Stepper Orientation')
        self.sail_plt.get_xaxis().set_visible(False)
        self.sail_plt.get_yaxis().set_visible(False)
        self.sail_arr = self.sail_plt.arrow(0, 0, 0, 0)

        self.rudder_fig = plt.figure()
        self.rudder_plt = self.rudder_fig.add_subplot(111, projection='polar')
        self.rudder_plt.set_title('Rudder Servo Orientation')
        self.rudder_plt.get_xaxis().set_visible(False)
        self.rudder_plt.get_yaxis().set_visible(False)
        self.rudder_arr = self.rudder_plt.arrow(0, 0, 0, 0)
        
    def run(self):
        """Runs controls integration test"""
        while True:
            # generate new positions
            sail_pos, rudder_pos = self.gen_positions()

            # set positions
            self.set_positions(sail_pos, rudder_pos)

            # plot expected positions
            self.plot_expected()

            # plot feedback positions (TODO)

            # sleep for update interval
            sleep(self.update_interval)

    def set_positions(self, sail_pos = 0, rudder_pos = 0):
        """
        Calls rudder and sail listener to set their respective positions
        Inputs:
            sail_pos -- position (in degrees from starboard) of sail
            rudder_pos -- position (in degrees from starboard) of rudder
        """
        pub.sendMessage("set trim", sail_pos)           # set sail angle
        pub.sendMessage("set rudder", rudder_pos)       # set rudder angle

        # set current positions
        # TODO -- remove and replace with feedback in future TODO
        self.sail_pos = sail_pos
        self.rudder_pos = rudder_pos

    def gen_positions(self):
        """
        Generates positions for rudder and sail based on test scheme
        Returns:
            set_sail_pos -- value to set sail position to
            set_rudder_pos -- value to set rudder position to
        """
        return self.gen_sail_position(), self.gen_rudder_position()
    
    def gen_sail_position(self):
        """
        Generates position for sail based on test scheme
        Returns:
            set_sail_pos -- value to set sail position to
        """
        set_sail_pos, overran_bounds = self._gen_postion(self.sail_pos, \
                                                           self.sail_dir * self.test_config['sail']['rotate_rate'], \
                                                           self.test_config['sail']['l_bound'], \
                                                           self.test_config['sail']['r_bound'])

        if overran_bounds:
            self.sail_dir *= -1

        return set_sail_pos

    def gen_rudder_position(self):
        """
        Generates position for rudder based on test scheme
        Returns:
            set_rudder_pos -- value to set rudder position to 
        """
        set_rudder_pos, overran_bounds = self._gen_postion(self.rudder_pos, \
                                                           self.rudder_dir * self.test_config['rudder']['rotate_rate'], \
                                                           self.test_config['rudder']['l_bound'], \
                                                           self.test_config['rudder']['r_bound'])

        if overran_bounds:
            self.rudder_dir *= -1

        return set_rudder_pos

    def _gen_position(self, cur_pos, dtheta, l_bound, r_bound):
        """
        Helper method to generate bounded position given dtheta and bounds
        Inputs:
            cur_pos -- current position of element
            dtheta -- change in bearing of element
            l_bound -- bound on left side
            r_bound -- bound on right side
        Returns:
            pos -- new position of element
            overran_bounds -- flag to indicate if element overran bounds
        """
        unbounded_new_pos = cur_pos + dtheta

        overran_bounds_l, overran_bounds_r = unbounded_new_pos < l_bound, unbounded_new_pos > r_bound

        if overran_bounds_l:
            pos = l_bound - (unbounded_new_pos % l_bound)
        elif overran_bounds_r:
            pos = r_bound - (unbounded_new_pos % r_bound)
        else:
            pos = unbounded_new_pos

        return pos, overran_bounds_l or overran_bounds_r

    def plot_expected(self):
        """
        Plots expected positions for sail and rudder
        """
#        self.sail_arr
