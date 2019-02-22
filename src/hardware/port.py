from enum import Enum
from abc import ABC, abstractmethod

import serial


class PortType(Enum):
    TESTABLE = 0,
    SERIAL = 1


class Port(ABC):
    """Interface for port communication."""

    def __init__(self, config):
        """ Creates a new port.

        Keyword arguments:
        name -- The string identifier for the port
        type -- The port type
        """
        self.port_name = config["port_name"]

    @abstractmethod
    def open(self):
        """ Opens/starts port. """
        pass

    @abstractmethod
    def read(self):
        """ Reads in next message from port. """
        pass

    @abstractmethod
    def close(self):
        """ Closes/stops port. """
        pass


class TestablePort(Port):
    """ Provides a port object to be used for testing."""

    def __init__(self, config):
        super().__init__(config)
        self.value = config.get("read_value") or 0

    def open(self):
        pass

    def read(self):
        return self.value

    def close(self):
        pass


class SerialPort(Port):
    """ Provides a serial port object."""

    def __init__(self, config, port):
        super().__init__(config)
        self.port = port

    def open(self):
        self.port.open()

    def read(self):
        """ Reads in message from serial port.

        Returns:
        The message read.
        """
        try:
            bytes = self.port.inWaiting()
        except:
            bytes = 0
        return self.port.read(size=bytes)

    def close(self):
        self.port.close()


def make_port(config, mock_port=None):
    """ Creates a new communication port.

    Keyword arguments:
    config -- A port configuration dictionary.
    mock_lib -- A mock port object for testing.

    Returns:
    The type of port specified in the config.
    """
    port_type = PortType[config.get("port_type")]
    if port_type == PortType.SERIAL:
        if mock_port is None:
            port = serial.Serial(
                port=config["port_name"],
                baudrate=config["baudrate"],
                timeout=config["timeout"])
            return SerialPort(config=config, port=port)
        return SerialPort(config=config, port=mock_port)
    else:
        return TestablePort(config=config)
