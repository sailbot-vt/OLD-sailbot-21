class RudderServoController(Servo):
    """Extends the Servo class with specifics to the Rudder application
    The Rudder has a negative min value and positive max value.
    """

    def __init__(self, pwm_pin, duty_min, duty_max, angle_min, angle_max, mechanical_advantage):
        """
        Initializes the RudderServoController object as an extenstion of Servo

        Keyword arguments:
        self -- The caller, the new servo class.
        pwm_pin -- The pin being used to control the servo.
        duty_min -- The duty to send the servo to the full left position
        duty_max -- The duty to send the servo to the full right position
        angle_min -- The minimum allowed angle.
        angle_max -- The maximum allowed angle.

        Side effects:
        - Initializes instance variables
        - Sends the rudder to 0 rudder_angle
        """
        servo = Servo(pwm_pin, duty_min, duty_max, angle_min, angle_max)
        self.mechanical_advantage = mechanical_advantage
        current_rudder_angle = 0
        rudder_goto(0)


    def rudder_angle_to_servo_angle(self, rudder_angle):
        """
        Method to return the servo angle for a given rudder angle.
        Assumes linear relationship

        Keyword arguments:
        rudder_angle -- The desired angle of the rudder

        Returns:
        The angle of the servo that correspondes to the rudder angle
        """
        mechanical_advantage = 1 #This may be necessary later, robably should inport from elsewhere
        return rudder_angle*self.mechanical_advantage

    def constrain_rudder_angle(self, rudder_angle):
        """
        Method to constrain the rudder angle to possible angles. Uses the min
        and the max of the servo and the mechanical_advantage to determine
        possible angles.

        Keyword arguments:
        rudder_angle -- The desired angle of the rudder

        Returns:
        The constrained_angle
        """
        if (rudder_angle*self.mechanical_advantage > servo.angle_max):
            return servo.angle_max/self.mechanical_advantage
        if (rudder_angle*self.mechanical_advantage < servo.angle_min):
            return servo.angle_min/self.mechanical_advantage
        return rudder_angle


    def rudder_goto(self, rudder_angle):
        """
        Method to send the rudder to a given angle. Uses rudder_angle_to_servo_angle
        to get the servo angle and sends that to the regular goto method.

        Keyword arguments:
        rudder_angle -- The desired angle of the rudder

        Side effects:
        Calls the goto method of the servo class

        """
        constrained_rudder_angle = constrain_rudder_angle(rudder_angle)
        servo.goto(rudder_angle_to_servo_angle(self, constrained_rudder_angle)
        return constrained_rudder_angle
        current_rudder_angle = constrained_rudder_angle

    def change_rudder_angle(self, delta_rudder_angle):
        """
        Method to change the rudder angle by a given delta_rudder_angle.

        Keyword arguments:
        self -- The caller
        delta_rudder_angle -- The change in angle to be processed

        Side effects:
        Calls the rudder_goto method with the constrained angle
        """
        rudder_goto(constrain_rudder_angle(current_rudder_angle+delta_rudder_angle))
