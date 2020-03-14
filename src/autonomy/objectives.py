from enum import Enum


class Objectives(Enum):

    """All of the different event definitions converted to enum"""

    ENTER_STARTING_GATE = 0  # Used in FleetRace, EnduranceRace, PrecisionNavigation, Payload, Collision Avoidance
    ROUND_BUOYS_CCW = 1  # Used in FleetRace, PrecisionNavigation
    ROUND_BUOYS_CCW_LOOPING = 2 # Used in EnduranceRace
    ENTER_SK_BOX = 3  # Used in StationKeeping
    STAY_IN_BOX = 4  # Used in StationKeeping
    LEAVE_BOX = 5  # Used in StationKeeping
    ENTER_SEARCH_AREA = 6  # Used in Search
    START_SEARCH_PATTERN = 7  # Used in Search
    TOUCH_ONE_BUOY = 8  # Used in Search
