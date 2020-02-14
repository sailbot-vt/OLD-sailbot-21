import math
from pubsub import pub


class Helmsman:
    """Steers the boat."""

    def __init__(self, rudder_gain):
        """Builds a new helmsman with the specified rudder gain"""
        self.rudder_gain = rudder_gain

    def turn_to(self, target_heading, boat):
        """Calculates and sets the rudder angle.

        Keyword arguments:
        self -- The caller, the instance
        target_heading -- The desired heading

        Side effects:
        - Sets instance variables
        """
        angle_to_turn = (target_heading - boat.current_heading) % 360

        # Will always execute 180 deg turns to starboard
        if angle_to_turn > 180:
            angle_to_turn -= 360

        pub.sendMessage("set rudder", degrees_starboard=self.rudder_angle_for(angle_to_turn))

    def rudder_angle_for(self, degrees_to_turn):
        """Gets the right rudder angle for the amount to turn.

        Applies gain specified in config. Gain satisfies

        gain = 10log(rudder_angle / degrees_to_turn)

        where log denotes the common (base 10) logarithm.
        """
        return math.pow(10, (self.rudder_gain * 0.1)) * degrees_to_turn
