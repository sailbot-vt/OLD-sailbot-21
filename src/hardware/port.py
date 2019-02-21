from enum import Enum
from abc import ABC, abstractmethod

import serial


class PortType(Enum):
    Testable = 0,
    Serial = 1


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
        pass

    @abstractmethod
    def read(self):
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


class SerialPort(Port):
    """ Provides a serial port object."""

    def __init__(self, config, port):
        # serial_lib used was pyserial
        super().__init__(config)
        self.baudrate = config["baudrate"]
        self.timeout = config["timeout"]
        self.port = port

    def open(self):
        self.port.open()

    def read(self):
        """ Reads in message from serial port.

        Returns:
        The message read or 'None' if nothing was read.
        """
        try:
            bytes = self.port.inWaiting()
        except:
            bytes = 0
        msg = self.port.read(size=bytes)
        if len(msg) < 2:
            return None
        return msg


def make_port(config, mock_lib=None):
    """ Creates a new communication port.

    Implements the factory design pattern.

    Keyword arguments:
    config -- A port configuration dictionary.

    Returns:
    The type of port specified in the config.
    """
    port_type = PortType[config.get("port_type") or "Testable"]
    if port_type == PortType.Serial:
        if mock_lib is None:
            # Default: parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS
            port = serial.Serial(
                port=config["port_name"],
                baudrate=config["baudrate"],
                timeout=config["timeout"])
            return SerialPort(config=config, port=port)
        return SerialPort(config=config, port=mock_lib)
    else:
        return TestablePort(config=config)
