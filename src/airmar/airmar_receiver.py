from src.airmar.airmar_processor import AirmarProcessor
from src.airmar.airmar_exceptions import InvalidIDException, UnsupportedIDException
from src.airmar.airmar_exceptions import InvalidSentenceException
from src.airmar.config_reader import read_pin_config, read_port_config, read_ids
from src.airmar.nmeaparser.nmea_parser import NmeaParser

from threading import Lock

class AirmarReceiver:
    """Defines an Airmar receiver that sends data to a processor."""

    def __init__(self, broadcaster, logger, 
        mock_bbio=None, mock_port=None):
        """Initializes a new airmar receiver.

        Keyword arguments:
        broadcaster -- The broadcaster object to publish data.
        logger -- logs warnings and errors from receiver.
        mock_bbio -- testable bbio library.
        mock_port -- testable port library.

        Returns:
        A new Airmar Receiver
        """
        self.parser = NmeaParser()
        self.ids = read_ids()
        self.is_running = False
        self.uart_pin = read_pin_config(mock_bbio=mock_bbio)
        self.port = read_port_config(mock_port=mock_port)
        self.logger = logger
        self.processor = AirmarProcessor(
            broadcaster=broadcaster, parser=self.parser)

    def start(self):
        """ Sets up uart pin and open port to start listening. 
        Enables sentences specified by ids field to airmar serial port."""
        # Setup port/pin
        self.uart_pin.setup()
        self.port.open()

        # Airmar specific sentence transmissions to airmar port.
        # Resumes sentence transmission
        self.port.write(
            "{}".format(self.parser.power(resume=1)).encode(self.port.encoding))
        
        # First, disable all transmissions
        self.port.write(
            "{}".format(self.parser.toggle(enable=0)).encode(self.port.encoding))
        toggles = self.parser.toggle(self.ids)
        for toggle in toggles:
            # Second, enable specified transmissions in config
            self.port.write("{}".format(toggle).encode(self.port.encoding))
        
        self.is_running = True

    def send_airmar_data(self):
        """ Sends nmea sentence from serial port to processor to broadcast data 
        
        Side effects:
        Updates logger with warnings and errors
        """
        sentence = self.port.read_line(terminator='\r\n')

        try:
            data = self.parser.parse(sentence)
            self.processor.update_airmar_data(nmea=data)

        except InvalidIDException:
            self.logger.write_msg(pin_name=self.uart_pin.pin_name,
            msg=r"WARNING Invalid SID: \"{}\"".format(sentence), 
            rw_state="r")
        except InvalidSentenceException:
            self.logger.write_msg(pin_name=self.uart_pin.pin_name,
            msg=r"WARNING Unable to parse \"{}\"".format(sentence), 
            rw_state="r")
        except UnsupportedIDException:
            self.logger.write_msg(pin_name=self.uart_pin.pin_name,
            msg=r"WARNING Unsupported ID: \"{}\"".format(sentence), 
            rw_state="r")
        except Exception as e:
            self.logger.write_msg(pin_name=self.uart_pin.pin_name,
            msg=r"ERROR Unhandled Exception\"{}\": \"{}\"".format(e, sentence), 
            rw_state="r")

    def stop(self):
        """ Stops the pin and port """
        # Suspends sentences.
        self.port.write(
            "{}".format(self.parser.power(resume=0)).encode(self.port.encoding))
       
        # cleanup and close ports and pins
        self.port.close()
        self.uart_pin.cleanup()
        self.is_running = False
