class Servo:
    """Provides an interface to a PWM-controlled servo."""

    def __init__(self, config):
        """
        Sets up the servo with specifics to the actual servo.

        Keyword arguments:
        config -- The servo config

        Side effects:
        - Initializes instance variables
        - Starts the PWM with the given pin
        - Sends the current_angle to the zero or straight position
        """
        self.pwm_pin = config["pin"]
        self.full_left_angle = config["full_left_angle"]
        self.full_right_angle = config["full_right_angle"]

        self.full_left_duty = config["full_left_duty"]
        self.full_right_duty = config["full_right_duty"]
        self.duty_span = self.full_right_duty - self.full_left_duty

        self.pwm_pin.start(self.pwm_pin, (100 - self.full_left_duty), 60.0)
        self.current_angle = 0
        self.turn_to(0)

    def turn_to(self, angle):
        """Method to send the servo to the given angle.

        Automatically constrains the angle to the servo's given limits.

        Keyword arguments:
        angle -- The desired angle

        Side effects:
        - Sets the duty cycle using the calc_duty_cycle()
        - Sends the physical servo to the angle
        - Sets the current_angle to the new angle
        """
        constrained_angle = self.constrain(angle,
                                           self.full_left_angle,
                                           self.full_right_angle)
        self.pwm_pin.set_duty_cycle(self.calc_duty_cycle(constrained_angle))
        self.current_angle = constrained_angle

    def change_servo_angle_by(self, delta_angle):
        """Method to change the servo relative to the current_angle.

        Keyword arguments:
        delta_angle -- The change in angle to be processed

        Side effects:
        - Changes the current_angle variable of the object
        """
        self.turn_to(self.current_angle + delta_angle)

    def calc_duty_cycle(self, angle):
        """Method to calculate the duty cycle given the attributes of the servo.

        Keyword argument:
        angle -- The desired angle.

        Returns:
        duty_cycle - The duty cycle for the given angle.
        """
        return 100 - ((angle / 180) * self.duty_span + self.full_left_duty)

    @staticmethod
    def constrain(val, min_val, max_val):
        """
        Method to constrain values to between the min_val and max_val.

        Keyword arguments:
        val -- The unconstrained value
        min_val -- The lowest allowed value
        max_val -- The highest allowed value
        """
        return min(max_val, max(min_val, val))
