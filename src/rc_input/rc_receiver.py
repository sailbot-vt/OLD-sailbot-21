from numpy import sign
from pubsub import pub

from src.navigation_mode import NavigationMode

import pdb

class RCReceiver:
    """Defines an RC receiver that sends data to a broadcaster."""

    def __init__(self, pins, ports):
        """Initializes a new ADC receiver.

        Keyword arguments:
        pins -- The pin map with keys 'TRIM', 'RUDDER', 'MODE1', and 'MODE2', 'UART_RX', 'UART_TX' associated with Pin objects.
        ports -- The port map with key 'UART'

        Returns:
        A new BBIOReceiver
        """
        self.pins = pins
        self.ports = ports
        self.data = {"RUDDER": None,
                     "TRIM"  : None,
                     "MODE1" : None,
                     "MODE2" : None}
        self.start_serial()

    def start_serial(self):
        """ Sets up uart pins and open ports to start transmitting and receiving"""

#        pdb.set_trace()

        self.pins['UART_RX'].setup()
        self.pins['UART_TX'].setup()
        self.ports['UART'].close()
        self.ports['UART'].open()

        self.is_running = True

    def close_serial(self):
        """ Closes serial interface"""        

        self.ports['UART'].close()

    def send_inputs(self):
        """Sends inputs to the broadcaster to be published."""

        self._get_inputs()

        if self._get_mode() == NavigationMode.MANUAL:
            pub.sendMessage("set rudder", degrees_starboard=self._get_rudder_input())
            pub.sendMessage("set trim", degrees_in=self._get_trim_input())
        pub.sendMessage("set nav mode", mode=self._get_mode())

    def _get_inputs(self):
        """ Gets RC data from Arduino over serial"""

        self.data = self._decode_input(self.ports['UART'].read_line())

    def _decode_input(self, line=''):
        """ Decodes RC data from arduino
        
        Keyword Arguments:
        line -- String containing serial data sent from Arudino

        Returns:
        data -- Dictionary containing RC data
        """

        rline = line[0:(line.rfind('\\'))]
        ldata = rline.split(',')

        data = {}
        data["RUDDER"] = float(ldata[0])
        data["TRIM"] = float(ldata[1])
        data["MODE1"] = float(ldata[2])
        data["MODE2"] = float(ldata[3])

        return data

    def _get_rudder_input(self):
        """Scales the rudder values from the raw value to degrees to starboard.

        Preconditions:
        raw_value is on a scale of 0 to max_value.

        Keyword arguments:
        raw_value -- The raw rudder input.

        Returns:
        The rudder input in degrees to starboard.
        """
        unscaled_value = self.data["RUDDER"]  # Between -1 and 1
        degrees_starboard = unscaled_value  * 80.0  # Between -80 and 80
        return degrees_starboard

    def _get_trim_input(self):
        """Scales the trim values from the raw value to degrees in.

        Keyword arguments:
        raw_value -- The raw trim input.

        Returns:
        The trim input in degrees trimming in.
        """
        unscaled_value = self.data["TRIM"]  # Between -1 and 1
        degrees_in = unscaled_value * 20.0  # Between -20 and 20
        return degrees_in

    def _get_mode(self):
        """Maps an input voltage to a navigation mode.

        Keyword arguments:
        input_voltage -- The input voltage.

        Returns:
        The navigation mode corresponding to the input voltage.
        """
        state = self.data["MODE1"]
        if state:
            return NavigationMode.AUTONOMOUS
        return NavigationMode.MANUAL

    def _get_set_waypoint(self):
        """Not mapped."""
        return self.data["MODE2"]


