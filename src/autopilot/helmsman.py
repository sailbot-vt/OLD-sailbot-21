from pubsub import pub


def turn_to(target_heading, boat):
    """Calculates and sets the rudder angle.

    Keyword arguments:
    self -- The caller, the instance
    target_heading -- The desired heading

    Side effects:
    - Sets instance variables
    """
    angle_to_turn = (target_heading - boat.heading) % 360

    if angle_to_turn > 180:
        angle_to_turn -= 360

    pub.sendMessage("set rudder", degrees_starboard=rudder_angle_for(angle_to_turn))


def rudder_angle_for(degrees_to_turn):
    """Gets the right rudder angle for the amount to turn"""
    return degrees_to_turn / 1.2
