from src.utils.data import constrain


class Rudder:
    """Directly controls the rudder."""

    def __init__(self, servo, config):
        """
        Initializes a Rudder.

        Keyword arguments:
        servo -- The servo controlling the rudder movement.
        config -- The rudder configuration details.

        Side effects:
        - Initializes instance variables
        """
        self.servo = servo
        self.full_port_angle = config["full_port_angle"]
        self.full_starboard_angle = config["full_starboard_angle"]
        self.mechanical_advantage = config["mechanical_adv"]
        self.current_rudder_angle = 0

    def rudder_angle_to_servo_angle(self, rudder_angle):
        """Method to return the servo angle for a given rudder angle.

        Keyword arguments:
        rudder_angle -- The desired angle of the rudder

        Returns:
        The angle of the servo that corresponds to the rudder angle
        """
        return rudder_angle * self.mechanical_advantage

    def turn_to(self, rudder_angle):
        """Method to send the rudder to a given angle. Uses rudder_angle_to_servo_angle
        to get the servo angle and sends that to the regular turn_to method.

        Keyword arguments:
        rudder_angle -- The desired angle of the rudder

        Side effects:
        Calls the turn_to method of the servo class
        """
        constrained_rudder_angle = constrain(rudder_angle,
                                             self.full_port_angle,
                                             self.full_starboard_angle)
        self.servo.turn_to(self.rudder_angle_to_servo_angle(constrained_rudder_angle))
        self.current_rudder_angle = constrained_rudder_angle
        print("Setting rudder angle to {0}\n".format(constrained_rudder_angle))

    def change_rudder_angle(self, delta_rudder_angle):
        """Method to change the rudder angle by a given delta_rudder_angle.

        Keyword arguments:
        delta_rudder_angle -- The change in angle to be processed

        Side effects:
        Calls the rudder_turn_to method with the constrained angle
        """
        self.turn_to(constrain(self.current_rudder_angle + delta_rudder_angle,
                               self.full_port_angle,
                               self.full_starboard_angle))
