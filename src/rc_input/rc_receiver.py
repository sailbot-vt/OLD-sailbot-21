from abc import ABC, abstractmethod


class RCReceiver(ABC):
    def read_receiver(self):
        """Reads receiver input."""
        self._read_input()


    @abstractmethod
    def _read_input(self):
        """Reads input from the RC receiver."""
        pass

    @abstractmethod
    def _scale_rudder_input(self, raw_value=0):
        """Scales the rudder values from the raw value to

        Keyword arguments:
        raw_value -- The raw rudder input.
        """
        pass

    @abstractmethod
    def _scale_trim_input(self, raw_value=0):
        """Scales the trim values from the raw value to

        Keyword arguments:
        raw_value -- The raw trim input.
        """
        pass

class OurReceiver(RCReceiver)