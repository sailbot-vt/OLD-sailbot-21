from threading import Thread, Lock
from time import sleep
import numpy as np

from pubsub import pub

from src.navigation_mode import NavigationMode
from src.autonomy.nav.tack_points import place_tacks
from src.autonomy.nav.course import Path

from src.autonomy.obstacle_avoidance.obstacle_avoidance import ObstacleAvoidance
from src.autonomy.movement.movement import Movement

from src.autonomy.nav.config_reader import read_nav_config, read_interval, read_tack_config
from src.autonomy.feature_extraction.config_reader import read_start_gate_config, read_round_buoy_config
from src.autonomy.objectives import Objectives

from src.autonomy.feature_extraction.find_start_gate import find_start_gate
from src.autonomy.feature_extraction.get_course_from_buoys import get_course_from_buoys

mutex = Lock()

class Captain(Thread):
    """Thread to manage autonomous navigation"""

    def __init__(self, objectives, tracker, boat, wind, event_config):
        """Builds a new captain thread."""
        super().__init__()

        self.objectives = objectives
        self.tracker = tracker
        self.boat = boat
        self.wind = wind

        # read configs
        self.nav_interval = read_interval()
        self.start_gate_config = read_start_gate_config()
        self.round_buoy_config = read_round_buoy_config()
        self.nav_config = read_nav_config()
        self.tack_config = read_tack_config()
        self.event_config = event_config

        # initialize objectives
        self.init_objectives()

        # set state vars
        self.is_active = True
        self.tacking = False

        # subscribe to nav mode and return home channels
        pub.subscribe(self.switch_mode, "set nav mode")
        pub.subscribe(self.return_home, "return home")

        # initialize and start obstacle avoidance thread
        self.obst_avoid = ObstacleAvoidance(tracker, boat)
        self.obst_avoid.start()

        # initialize movement thread
        self.move = Movement(wind)
        self.move.start()

        self.path = Path()          # contains all waypoints and tack points
        self.waypoints = Path()     # only contains waypoints (no tack points) 

    def run(self):
        """Runs the captain thread"""
        while self.is_active:
            # update objectives
            self.update_objectives()

            # update course
            self.update_course()

            # place tacks on current leg
#            self.place_tacks()

            # set turn speed
            self.set_turn_speed()

            # set heading
            self.set_heading()

            # sleep
            sleep(self.nav_interval)

    def set_turn_speed(self):
        """
        Sets turn speed based on range and bearing of next waypoint
        """
        mark = self.path.next_mark()
        # generate turn speed weight (higher weights for more urgent turns (closer objs, further in bearing))
        if mark is not None:
            if mark[0] < 200:
                weight = (np.fabs(mark[1]) / 190.) + ((200 - mark[0]) / 3800.)
            else:
                weight = 0

            pub.sendMessage('set turn speed', turn_speed_factor = weight)

    def set_heading(self):
        """
        Sets heading for next mark
        """
        # set heading to next mark
        mark = self.path.next_mark()
        if mark is not None:
            pub.sendMessage('update waypoint', new_waypoint=mark)

    def place_tacks(self):
        """
        Places tacks for current leg
        Side Effects:
            self.path -- inserts tacks into course
            self.tacking -- updates to reflect if tacking is occurring or not
        """
        # check if necessary to tack, if necessary to switch tacks
        tack_flag, switch_tack_flag = self.tack_in_progress()

        if not tack_flag:
            # prepend tacks to course
            mark = self.path.next_mark()
            if mark is not None:
                tacks = place_tacks(mark, self.boat, self.wind, self.tack_config, switch_tack_flag)

                for tack in tacks[::-1]:
                    self.path.prepend_mark(tack)

                if len(tacks) > 1:
                    self.tacking = True
                else:
                    self.tacking = False

    def tack_in_progress(self):
        """
        Finds if a tack leg is in progress and if switching tacks is necessary
        Returns:
            tack_in_progress -- bool that returns True if tack point is not yet reached
            switch_tack -- bool that returns true if necessary to switch tacks
        """
        tack_point = self.path.next_mark()
        if self.tacking == True and tack_point is not None:
            if tack_point[0] < self.tack_config['tack_point_width']:
                return False, True
            else:
                return True, False

        return False, False

    def update_course(self):
        """
        Updates course based on new buoy positions, new/updated objectives
        Side Effects:
            self.path -- updates path 
            self.waypoints -- adds waypoints
        """
        # get buoys from tracker
        buoys = self.tracker.get_buoys()

        # reset course
        self.clear_path()

        # iterate through objectives
        mutex.acquire()
        for objective in self.objectives:
            self.add_marks_for_objective(objective, buoys)
        mutex.release()

    def add_marks_for_objective(self, objective, buoys):
        """
        Adds marks to course for objective
        Inputs:
            objective -- enumerated objective to be accomplished
            buoys -- array of buoy locations
        Side Effects:
            self.path -- updates course
        """
        if objective == Objectives.ENTER_STARTING_GATE:
            # find start gate
            centerpoint, _ = find_start_gate(buoys, self.start_gate_config)

            # add mark for gate
            if centerpoint is not None:
                self.add_marks(centerpoint)
            
        elif objective == Objectives.ROUND_BUOYS_CCW:
            # find gate buoys
            _ , buoys_used = find_start_gate(buoys, self.start_gate_config)
            gate_buoys = [True if buoy in buoys_used else False for buoy in buoys]

            # trim buoy array to non-gate buoys
            buoy_array = [buoy for buoy, gate_buoy in zip(buoys, gate_buoys) if gate_buoy is False]

            # sort buoys CCW
            sorted_buoys = get_course_from_buoys(buoy_array, 'CCW')

            if len(sorted_buoys) > 0:
                # generate marks (using margin from config)
                rng_margin = self.round_buoy_config['rng_margin']
                bearing_margin = self.round_buoy_config['bearing_margin']
                marks = [(rng + rng_margin, bearing + bearing_margin) for (rng, bearing) \
                                                                      in sorted_buoys[0:self.buoys_left_in_loop]]

                # add marks for buoys
                self.add_marks(marks)
            
        elif objective == Objectives.ROUND_BUOYS_CCW_LOOPING:
            pass
        elif objective == Objectives.ENTER_SK_BOX:
            pass
        elif objective == Objectives.STAY_IN_BOX:
            pass
        elif objective == Objectives.LEAVE_BOX:
            pass
        elif objective == Objectives.ENTER_SEARCH_AREA:
            pass
        elif objective == Objectives.START_SEARCH_PATTERN:
            pass
        elif objective == Objectives.TOUCH_BUOY:
            pass

    def update_objectives(self):
        """
        Updates objectives based on objectives attained
        Side Effects:
            self.objectives -- updates objectives
        """
        objective_attained = False

        mutex.acquire()

        # get objective and waypoint
        objective = self.objectives[0]
        waypoint = self.waypoints.next_mark()

        if objective == Objectives.ENTER_STARTING_GATE:
            if waypoint is not None:
                if waypoint[0] < self.nav_config['mark_width']:   # delete start gate objective if start gate within margin
                    del self.objectives[0]

                    objective_attained = True

        elif objective == Objectives.ROUND_BUOYS_CCW:
            if waypoint is not None:
                if waypoint[0] < self.nav_config['mark_width']:
                    self.buoys_left_in_loop -= 1

                    if self.buoys_left_in_loop == 0:
                        del self.objectives[0]

                        objective_attained = True
            
        elif objective == Objectives.ROUND_BUOYS_CCW_LOOPING:
            pass
        elif objective == Objectives.ENTER_SK_BOX:
            pass
        elif objective == Objectives.STAY_IN_BOX:
            pass
        elif objective == Objectives.LEAVE_BOX:
            pass
        elif objective == Objectives.ENTER_SEARCH_AREA:
            pass
        elif objective == Objectives.START_SEARCH_PATTERN:
            pass
        elif objective == Objectives.TOUCH_BUOY:
            pass

        mutex.release()

    def init_objectives(self):
        """
        Initializes state for objectives
        """
        mutex.acquire()

        for objective in self.objectives:
            if objective == Objectives.ENTER_STARTING_GATE:
                pass
            elif objective == Objectives.ROUND_BUOYS_CCW:
                self.buoys_left_in_loop = self.event_config['num_loop_buoys']
            elif objective == Objectives.ROUND_BUOYS_CCW_LOOPING:
                pass
            elif objective == Objectives.ENTER_SK_BOX:
                pass
            elif objective == Objectives.STAY_IN_BOX:
                pass
            elif objective == Objectives.LEAVE_BOX:
                pass
            elif objective == Objectives.ENTER_SEARCH_AREA:
                pass
            elif objective == Objectives.START_SEARCH_PATTERN:
                pass
            elif objective == Objectives.TOUCH_BUOY:
                pass

        mutex.release()

    def return_home(self):
        """
        Updates objectives to return home as next mark
        Side Effects:
            self.objectives -- updates objectives
        """
        mutex.acquire()
        mutex.release()

    def switch_mode(self, mode):
        """Changes the navigation mode"""
        if mode is NavigationMode.AUTONOMOUS:
            self.enable()
        else:
            self.disable()

    def disable(self):
        """Disables the autonomous navigation"""
        self.is_active = False
        self.path.clear()

    def enable(self):
        """Enables the autonomous navigation"""
        self.is_active = True

    def clear_path(self):
        """
        Clears path and waypoints
        Side Effects:
            self.path -- clears all waypoints
            self.waypoints -- clears all waypoints
        """
        self.path.clear()
        self.waypoints.clear()

    def add_marks(self, marks):
        """
        Adds mark(s) to course
        Inputs:
            marks -- list of (or single) mark(s) to add to course
        Side Effects:
            self.path -- updates course
        """
        if isinstance(marks, list):
            for mark in marks:
                self.path.add_mark(mark)
                self.waypoints.add_mark(mark)
        else:
            self.path.add_mark(marks)
            self.waypoints.add_mark(marks)
