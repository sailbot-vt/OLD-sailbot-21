from threading import Thread, Lock
from time import sleep
import numpy as np

from pubsub import pub

from src.navigation_mode import NavigationMode
from src.autonomy.nav.tack_points import place_tacks
from src.autonomy.nav.course import Path

from src.autonomy.obstacle_avoidance.obstacle_avoidance import ObstacleAvoidance
from src.autonomy.movement.movement import Movement
from src.autonomy.movement.turn_speed_enum import TurnSpeed

from src.autonomy.nav.config_reader import read_nav_config, read_interval, read_tack_config
from src.autonomy.feature_extraction.config_reader import read_start_gate_config, read_round_buoy_config
from src.autonomy.objectives import Objectives

from src.autonomy.feature_extraction.find_start_gate import find_start_gate
from src.autonomy.feature_extraction.get_course_from_buoys import get_course_from_buoys

mutex = Lock()

class Captain(Thread):
    """Thread to manage autonomous navigation"""

    def __init__(self, objectives, tracker, boat, wind):
        """Builds a new captain thread."""
        super().__init__()

        self.objectives = objectives
        self.tracker = tracker
        self.boat = boat
        self.wind = wind

        self.is_active = True
        self.nav_interval = read_interval()
        self.start_gate_config = read_start_gate_config()
        self.round_buoy_config = read_round_buoy_config()
        self.nav_config = read_nav_config()
        self.tack_config = read_tack_config()

        pub.subscribe(self.switch_mode, "set nav mode")
        pub.subscribe(self.return_home, "return home")

        # initialize and start obstacle avoidance thread
        self.obst_avoid = ObstacleAvoidance(tracker, boat)
        self.obst_avoid.start()

        # initialize movement thread
        self.move = Movement(wind)
        self.move.start()

        self.path = Path()

    def run(self):
        """Runs the captain thread"""
        while self.is_active:
            # update course
            self.update_course()

            # place tacks on current leg
#            self.place_tacks()

            # set turn speed
            self.set_turn_speed()

            # set heading
            self.set_heading()

            # update objectives
            self.update_objectives()

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
                weight = (np.fabs(mark[1]) / 200.) + ((200 -mark[0]) / 2000.)  # 9x weight on bearing vs range -- linear scale
            else:
                weight = 0

            print(weight, mark)
            if weight < 0.15:
                pub.sendMessage('set turn speed', turn_speed=TurnSpeed.VERYSLOW)
            elif 0.15 <= weight < 0.35:
                pub.sendMessage('set turn speed', turn_speed=TurnSpeed.SLOW)
            elif 0.35 <= weight < 0.65:
                pub.sendMessage('set turn speed', turn_speed=TurnSpeed.MEDIUM)
            elif 0.65 <= weight < 0.85:
                pub.sendMessage('set turn speed', turn_speed=TurnSpeed.FAST)
            else:
                pub.sendMessage('set turn speed', turn_speed=TurnSpeed.VERYFAST)

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
        """
        # prepend tacks to course
        mark = self.path.next_mark()
        if mark is not None:
            tacks = place_tacks(mark, self.boat, self.wind, self.tack_config)

            for tack in tacks[::-1]:
                self.path.prepend_mark(tack)

    def update_course(self):
        """
        Updates course based on new buoy positions, new/updated objectives
        Side Effects:
            self.path -- updates course
        """
        # get buoys from tracker
        buoys = self.tracker.get_buoys()
        self.gate_buoys = [0] * len(buoys)

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
            self.gate_buoys -- updates to reflect buoys used as gates
        """
        if objective == Objectives.ENTER_STARTING_GATE:
            # find start gate
            centerpoint, buoys_used = find_start_gate(buoys, self.start_gate_config)
            self.gate_buoys = [True if buoy in buoys_used else False for buoy in buoys]

            # add mark for gate
            if centerpoint is not None:
                self.add_marks(centerpoint)
            
        elif objective == Objectives.ROUND_BUOYS_CCW:
            # find gate buoys
            _ , buoys_used = find_start_gate(buoys, self.start_gate_config)
            self.gate_buoys = [True if buoy in buoys_used else False for buoy in buoys]

            # trim buoy array to non-gate buoys
            buoy_array = [buoy for buoy, gate_buoy in zip(buoys, self.gate_buoys) if gate_buoy is False]

            # sort buoys CCW
            sorted_buoys = get_course_from_buoys(buoy_array, 'CCW')

            if len(sorted_buoys) > 0:
                # generate marks (using margin from config)
                rng_margin = self.round_buoy_config['rng_margin']
                bearing_margin = self.round_buoy_config['bearing_margin']
                marks = [(rng + rng_margin, bearing + bearing_margin) for (rng, bearing) in sorted_buoys]

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
        mutex.acquire()
        objective = self.objectives[0]
        if objective == Objectives.ENTER_STARTING_GATE:
            mark  = self.path.next_mark()
            if mark is not None:
                if mark[0] < self.nav_config['mark_width']:         # delete start gate objective if start gate within margin
                    del self.objectives[0]
                    print(self.objectives)

        elif objective == Objectives.ROUND_BUOYS_CCW:
            pass
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
        self.path = Path()

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
        else:
            self.path.add_mark(marks)
