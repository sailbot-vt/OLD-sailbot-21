from src.utils.data import constrain
from pubsub import pub


class Mainsheet:
    """Controls the mainsheet."""

    def __init__(self, config):
        """
        Initializes the Mainsheet object

        Keyword arguments:
        config -- The mainsheet configuration

        Side effects:
        - Initializes instance variables
        - Sends the boom to 0 boom_angle
        """

        self.max_boom_angle = config["max_boom_angle"]
        self.sheeting_adv = config["sheeting_adv"]

        self.current_boom_angle = 0
        self.trim_boom_to(0)

    def boom_angle_to_motor_angle(self, boom_angle):
        """Method to return the motor angle for a given sail angle.

        Keyword arguments:
        boom_angle -- The desired angle of the boom

        Returns:
        The angle of the motor that corresponds to the sail angle
        """

        # TODO: Figure out trig for boom movement vs. sheet movement
        return (boom_angle - self.max_boom_angle * 0.5) * self.sheeting_adv

    def trim_boom_to(self, boom_angle):
        """Sends the boom to a given angle.

        Uses sail_angle_to_motor_angle to get the motor angle and sends that to
        the motor's turn_to method.

        Keyword arguments:
        sail_angle -- The desired boom angle

        Returns:
        The constrained boom angle that the motor was set to

        Side effects:
        Calls the turn_to method of the motor class
        """
        constrained_boom_angle = constrain(boom_angle, 0, self.max_boom_angle)
        pub.sendMessage("turn sail to", sail_ang=self.boom_angle_to_motor_angle(constrained_boom_angle))
        self.current_boom_angle = constrained_boom_angle
        return constrained_boom_angle

    def trim_in_by(self, degrees_in):
        """Method to change the sail angle by a given delta_sail_angle.

        Keyword arguments:
        delta_sail_angle -- The change in angle to be processed

        Side effects:
        Calls the sail_turn_to method with the constrained angle
        """
        self.trim_boom_to(constrain(self.current_boom_angle + degrees_in,
                                    0,
                                    self.max_boom_angle))
