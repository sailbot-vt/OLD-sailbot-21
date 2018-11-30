from src.servo import Servo

class SailServoController:
    """
    The sail has no negative values as 0 is parralel with the keel and
    positive can be either direction as the wind decides.
    """

    def __init__(self, pwm_pin, duty_min, duty_max, angle_min, angle_max):
        """
        Initializes the SailServoController object

        Keyword arguments:
        self -- The caller, the new servo class.
        pwm_pin -- The pin being used to control the servo.
        duty_min -- The duty to send the servo to the full left position
        duty_max -- The duty to send the servo to the full right position
        angle_min -- The minimum allowed angle.
        angle_max -- The maximum allowed angle.
        pwm_lib -- The Adafruit_BBIO PWM library or mock.

        Side effects:
        - Initializes instance variables
        - Creates a servo object
        - Sends the sail to 0 sail_angle
        """

        self.servo = Servo(pwm_pin, duty_min, duty_max, angle_min, angle_max)
        self.current_sail_angle = 0
        self.sail_turn_to(0)

    def sail_angle_to_servo_angle(self, sail_angle):
        """
        Method to return the servo angle for a given sail angle.

        TODO: Add a way to account for the non-linear relationship between the
        servo and the sail.

        Keyword arguments:
        self -- The caller
        sail_angle -- The desired angle of the sail

        Returns:
        The angle of the servo that correspondes to the sail angle
        """
        return self.servo.angle_min + (self.servo.angle_max - self.servo.angle_min) * (sail_angle/90)

    def constrain_sail_angle(self, sail_angle):
        """
        Method to constrain the sail_angle to between 0 and 90

        Keyword arguments:
        sail_angle -- The angle to be constrained

        Returns:
        The constrained angle.
        """
        min = 0
        max = 90
        if (sail_angle<min):
            return min
        if (sail_angle>max):
            return max

    def sail_turn_to(self, sail_angle):
        """
        Method to send the sail to a given angle. Uses sail_angle_to_servo_angle
        to get the servo angle and sends that to the regular turn_to method.

        Keyword arguments:
        self -- The caller
        sail_angle -- The desired angle of the sail

        Returns:
        The constrained sail angle that the servo was set to

        Side effects:
        Calls the turn_to method of the servo class

        """
        constrained_sail_angle = self.constrain_sail_angle(sail_angle)
        self.servo.turn_to(self.sail_angle_to_servo_angle(constrained_sail_angle))
        self.current_sail_angle = constrained_sail_angle
        return constrained_sail_angle

    def change_sail_angle(self, delta_sail_angle):
        """
        Method to change the sail angle by a given delta_sail_angle.

        Keyword arguments:
        self -- The caller
        delta_sail_angle -- The change in angle to be processed

        Side effects:
        Calls the sail_turn_to method with the constrained angle
        """
        self.sail_turn_to(self.constrain_sail_angle(self.current_sail_angle+delta_sail_angle))
