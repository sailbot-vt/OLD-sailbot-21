from threading import Thread

from pubsub import pub
from time import sleep
from numpy import sign, exp

from src.autonomy.movement.config_reader import read_movement_config

class Movement(Thread):
    """Movement control thread"""
    def __init__(self, wind):
        """
        Initializes movement object 
        Inputs:
            wind -- wind object containing wind state data
        """
        super().__init__()
        self.wind = wind

        self.config = read_movement_config()
        self.update_interval = self.config['update_interval']
        self.max_rudder_ang = self.config['rudder_angles']['max_rudder_ang']
        self.rudder_angle = 0.5 * self.max_rudder_ang

        pub.subscribe(self.set_heading, "set heading")
        pub.subscribe(self.set_turn_speed, "set turn speed")

        self.is_active = True

    def run(self):
        """
        Runs movement thread
        """
        while self.is_active:
            # set sail and jib for max lift
            self.set_sail()
            self.set_jib()

            sleep(self.update_interval)

    def quit(self):
        """
        Quits movement thread
        """
        self.is_active = False

    def set_turn_speed(self, turn_speed_factor):
        """
        Sets turn speed
        Inputs:
            turn_speed_factor -- turn speed factor to achieve (affects rudder angle)
        Side Effects:
            self.rudder_angle -- updates rudder angle
        """
        self.rudder_angle = self.max_rudder_ang * exp(turn_speed_factor**2 - 1)

    def set_heading(self, adjusted_heading):
        """
        Sets rudder for maneuver
        Inputs:
            adjusted_heading -- heading to adjust to
        """
        # set rudder
        self.set_rudder(adjusted_heading)

    def set_rudder(self, heading):
        """
        Sets rudder for desired heading
        Inputs:
            heading -- desired heading to turn to
        """
        turn_to = sign(heading) * self.rudder_angle
        pub.sendMessage("set rudder", degrees_starboard = turn_to)

    def set_sail(self):
        """
        Sets sail for max lift
        """
        pass

    def set_jib(self):
        """
        Sets jib for max lift
        """
        pass
