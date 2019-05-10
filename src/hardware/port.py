from abc import ABC, abstractmethod
from enum import Enum

import re
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
    def read_line(self, terminator='\n'):
        """ Reads in next line from port. """
        pass

    @abstractmethod
    def write(self, msg):
        """ Writes message to port. """
        pass

    @abstractmethod
    def close(self):
        """ Closes/stops port. """
        pass

    @abstractmethod
    def is_open(self):
        """ Checks if the port is opened.

        Returns:
        True if port is open.
        """
        pass


class TestablePort(Port):
    """ Provides a port object to be used for testing."""

    def __init__(self, config):
        super().__init__(config)
        self.value = config.get("read_value") or 0

    def open(self):
        pass
        
    def is_open(self):
        pass

    def write(self, msg):
        return msg

    def read_line(self, terminator='\n'):
        return self.value + terminator

    def read(self):
        return self.value

    def close(self):
        pass


class SerialPort(Port):
    """ Provides a serial port object."""

    def __init__(self, config, port):
        super().__init__(config)
        self.encoding = config["encoding"]
        self.port = port
        self.remaining_input = ""

    def open(self):
        if not self.is_open():
            self.port.open()

    def write(self, msg):
        self.port.write(msg)

    def is_open(self):
        return self.port.isOpen()

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

    def read_line(self, terminator='\n'):
        """ Reads in next line from serial port.

        Returns:
        line as a string, None if port not opened.
        """
        while self.is_open():
            line = ""
            if self.remaining_input:
                line = self.remaining_input
                self.remaining_input = ""
            
            next_bytes = self.read().decode(self.encoding)
            if next_bytes:
                line += next_bytes

            if re.search(terminator, line):
                data, self.remaining_input = line.split(terminator, 1)
                line = ""
                # appends terminator back
                return data + terminator
        return None


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
