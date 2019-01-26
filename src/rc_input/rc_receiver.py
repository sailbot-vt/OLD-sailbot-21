from numpy import sign

from src.navigation_mode import NavigationMode


class RCReceiver:
    """Defines an RC receiver that sends data to a broadcaster."""

    def __init__(self, broadcaster, pins):
        """Initializes a new ADC receiver.

        Keyword arguments:
        broadcaster -- An RC broadcaster object.
        pins -- The pin map with keys 'TRIM', 'RUDDER', 'MODE1', and 'MODE2' associated with Pin objects.

        Returns:
        A new BBIOReceiver
        """
        self.broadcaster = broadcaster
        self.pins = pins

    def send_inputs(self):
        """Sends inputs to the broadcaster to be published.

        Keyword arguments:
        inputs – Inputs to be sent. A dictionary with keys 'RUDDER', 'TRIM', and 'MODE'
        """
        self.broadcaster.move_rudder(degrees_starboard=self._get_rudder_input())
        self.broadcaster.change_trim(degrees_in=self._get_trim_input())
        self.broadcaster.change_mode(mode=self._get_mode())

    def _get_rudder_input(self):
        """Scales the rudder values from the raw value to degrees to starboard.

        Preconditions:
        raw_value is on a scale of 0 to max_value.

        Keyword arguments:
        raw_value -- The raw rudder input.

        Returns:
        The rudder input in degrees to starboard.
        """
        unscaled_value = self.pins["RUDDER"].read()  # Between -1 and 1
        degrees_starboard = sign(unscaled_value) * 80 * (unscaled_value ** 2)  # Between -80 and 80
        return degrees_starboard

    def _get_trim_input(self):
        """Scales the trim values from the raw value to degrees in.

        Keyword arguments:
        raw_value -- The raw trim input.

        Returns:
        The trim input in degrees trimming in.
        """
        unscaled_value = self.pins["TRIM"].read()  # Between -1 and 1
        degrees_in = sign(unscaled_value) * 20 * (unscaled_value ** 2)  # Between -20 and 20
        return degrees_in

    @staticmethod
    def _get_mode():
        """Maps an input voltage to a navigation mode.

        Keyword arguments:
        input_voltage -- The input voltage.

        Returns:
        The navigation mode corresponding to the input voltage.
        """
        return NavigationMode.MANUAL

