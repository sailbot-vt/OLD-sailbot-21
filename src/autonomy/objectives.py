from enum import Enum


class Objectives(Enum):

    """All of the different event definitions converted to enum"""

    ENTER_STARTING_GATE = 0  # Used in FleetRace, EnduranceRace, PrecisionNavigation, Payload, Collision Avoidance
    ROUND_BUOYS_CCW = 1  # Used in FleetRace, EnduranceRace, PrecisionNavigation
    RETURN_TO_STARTING_GATE = 2  # Used in FleetRace, EnduranceRace, PrecisionNavigation, Payload, Collision Avoidance
    ENTER_SK_BOX = 3  # Used in StationKeeping
    STAY_IN_BOX = 4  # Used in StationKeeping
    LEAVE_BOX = 5  # Used in StationKeeping
    ROUND_ONE_BUOY = 6  # Used in Payload, CollisionAvoidance
    ENTER_SEARCH_AREA = 7  # Used in Search
    START_SEARCH_PATTERN = 8  # Used in Search
    PASS_ALONG_SIGNAL = 9  # Used in Search
    TOUCH_ONE_BUOY = 10  # Used in Search,
