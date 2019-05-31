from enum import Enum


class SailType(Enum):
    """Types of sails"""
    MAIN = 0,
    FRACTIONAL_J0 = 1,
    FOIL = 2


def make_sail(type):
    pass
