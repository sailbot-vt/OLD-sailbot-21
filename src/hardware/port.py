from enum import Enum
from abc import ABC, abstractmethod


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

    def __init__(self, name, read_value):
        self.pin_name = name
        self.value = read_value

    def open(self):
        pass

    def read(self):
        return self.value


class SerialPort(Port):
    """ Provides a serial port object."""

    def __init__(self, config, serial_lib):
        # serial_lib used was pyserial
        super().__init__(config)
        self.baudrate = config["baudrate"]
        self.timeout = config["timeout"]
        self.port = serial_lib.Serial(
            port=self.port_name, baudrate=self.baudrate, timeout=self.timeout)
        # Default: parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS

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
    """ Cretes a new communication port.

    Implements the factory design pattern.

    Keyword arguments:
    config -- A port configuration dictionary.

    Returns:
    The type of port specified in the config.
    """
    port_type = PortType[config.get("port_type") or "Testable"]
    if port_type == PortType.Serial:
        if mock_lib is None:
            import serial as serial_lib
            return SerialPort(config=config, serial_lib=serial_lib)
        return SerialPort(config=config, serial_lib=mock_lib)
    else:
        return TestablePort(name=config["port_name"], read_value=config.get("read_value") or 0)
