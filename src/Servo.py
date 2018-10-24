
class Servo()
    """
    Import the Adafruit_BBIO PWM library.
    General sero class to control a general servo.
    """
    PWM = __input__(Adafruit_BBIO.PWM)

    def __init__(self, pwm_pin, duty_min, duty_max, angle_min, angle_max):
        """
        Sets up the servo with specifics to the actual servo.

        Keyword arguments:
        self -- The caller, the new servo class.
        pwm_pin -- The pin being used to control the servo.
        duty_min -- The duty to send the servo to the full left position
        duty_max -- The duty to send the servo to the full right position
        angle_min -- The minimum allowed angle.
        angle_max -- The maximum allowed angle.

        Side effects:
        - Initializes instance variables
        - Starts the PWM with the given pin
        - Sends the current_angle to the zero or straight position
        """
        self.pwm_pin = pwm_pin
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty_span = duty_max-duty_min
        self.angle_min = angle_min
        self.angle_max = angle_max
        PWM.start(self.pwm_pin,(100-duty_min), 60.0)
        self.current_angle = goto(0)

    def goto(self, angle):
        """
        Method to send the servo to the given angle.

        Keyword arguments:
        self -- The caller
        servo_angle -- The desired angle

        Side effects:
        - Sets the duty cycle using the calc_duty_cycle()
        - Sends the physical servo to the angle
        - Sets the current_angle to the

        Returns:
        - Returns the angle that the servo went to
        """
        constrained_angle = constrain(self.angel_min, self.angle_max, angle)
        PWM.set_duty_cycle(self.pwm_pin, calc_duty_cycle(constrained_angle)
        self.current_angle = constraied_angle;
        return constrain_angle

    def changeServoAngle(self, deltaAngle):
        """
        Method to change the servo relative to the current_angle

        Keyword arguments:
        self -- The caller
        deltaAngle -- The change in angle to be processed

        Side effects:
        - Changes the current_angle varaible of the object
        """
        self.current_angle = goto(self.current_angle+deltaAngle)

    def calc_duty_cycle(angle):
        """
        Method to calculate the duty cycle given the attributes of the servo.

        Keyword argument:
        angle -- The desired angle.

        Returns:
        duty_cycle - The duty cycle for the given angle.
        """
        return 100 - ((angle / 180) * duty_span + self.duty_min)

    def constrain(min, max, angle):
        """
        Method to constrain angles to between the min and max values

        Keyword arguments:
        min -- the lowest allowed value for the angle
        max -- the highest allowed value for the angle
        angle -- the unconstrained angle to be constrained


        """
        if(angle>max):
            return max
        if(angle<min):
            return min
        return min
