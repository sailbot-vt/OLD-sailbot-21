from enum import Enum


class PinType(Enum):
    """An enum type to denote the type of pin"""
    GPIO = 0,
    ADC = 1


class Pin:
    """Holds information about a BBB pin."""

    def __init__(self, name, pin_type):
        """Creates a new pin.

        Keyword arguments:
        name -- The string identifier for the pin
        type -- The pin type
        """
        self.name = name
        self.pin_type = pin_type
