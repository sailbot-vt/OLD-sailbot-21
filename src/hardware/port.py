from enum import Enum
import abc import ABC, abstractmethod

class PortType(Enum):
    Testable = 0,
    Serial = 1,
    USB = 2


class Port(ABC):
    """Interface for port communication."""

    def __init__(self, config):
        """ Creates a new port.

        Keyword arguments:
        name -- The string identifier for the port
        type -- The port type
        """
        self.port_name = config["port_name"]


class TestablePort(Port):
    """ Provides a port object to be used for testing."""

    def __init__(self, name, read_value):
        self.pin_name = name
        self.value = read_value
        self.written_values = []

    def read(self):
        return self.value

    def set_state(self, state):
        self.written_values.append(state)

    def start(self, *args):
        pass

    def stop(self):
        pass

    class SerialPort(Port):

        def __init__(self, config, serial_lib):
            super().__init__(config)

            self.baudrate = config["baudrate"]
            self.timeout = config["timeout"]
