from numpy import sign
from pubsub import pub

from src.navigation_mode import NavigationMode

class RCReceiver:
    """Defines an RC receiver that sends data to a broadcaster."""

    def __init__(self, pins):
        """Initializes a new ADC receiver.

        Keyword arguments:
        pins -- The pin map with keys 'TRIM', 'RUDDER', 'MODE1', and 'MODE2' associated with Pin objects.

        Returns:
        A new BBIOReceiver
        """
        self.pins = pins

    def send_inputs(self):
        """Sends inputs to the broadcaster to be published.

        Keyword arguments:
        inputs – Inputs to be sent. A dictionary with keys 'RUDDER', 'TRIM', and 'MODE'
        """

        if self._get_mode() == NavigationMode.MANUAL:
            pub.sendMessage("set rudder", degrees_starboard=self._get_rudder_input())
            pub.sendMessage("set trim", degrees_in=self._get_trim_input())
        pub.sendMessage("set nav mode", mode=self._get_mode())

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
        degrees_starboard = unscaled_value  * 80.0  # Between -80 and 80
        return degrees_starboard

    def _get_trim_input(self):
        """Scales the trim values from the raw value to degrees in.

        Keyword arguments:
        raw_value -- The raw trim input.

        Returns:
        The trim input in degrees trimming in.
        """
        unscaled_value = self.pins["TRIM"].read()  # Between -1 and 1
        degrees_in = unscaled_value * 20.0  # Between -20 and 20
        return degrees_in

    def _get_mode(self):
        """Maps an input voltage to a navigation mode.

        Keyword arguments:
        input_voltage -- The input voltage.

        Returns:
        The navigation mode corresponding to the input voltage.
        """
        state = self.pins["MODE1"].read()
        if state:
            return NavigationMode.AUTONOMOUS
        return NavigationMode.MANUAL

    def _get_set_waypoint(self):
        """Not mapped."""
        return self.pins["MODE2"].read()


