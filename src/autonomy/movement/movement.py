from threading import Thread

from pubsub import pub
from time import sleep
from numpy import sign

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

        config = read_movement_config()
        self.update_interval = config['update_interval']
        self.rudder_angle = config['rudder_angles'][config['default_turn_rate']]

        pub.subscribe(self.set_heading, "set heading")

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
        pub.sendMessage("set rudder", turn_to)

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
