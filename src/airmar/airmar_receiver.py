import pynmea2

class AirmarReceiver:
    def __init__(self, pin, port):
        self.uart_pin = pin
        self.port = port
        self.processor = AirmarProcessor()

    def start(self):
        self.uart_pin.setup()
        self.port.open()
        # self.processor.update_data(self._sanitize_line())

    def send_data(self):
        # PyPubsub or keep as a dict?
        msg = self._read_msg()
        if msg is not None:
            data = pynmea2.parse(msg)
            self.processor.update_data(data=data)

    def _read_msg(self):
        raw_msg = self._read_raw_data()
        msg = self._sanitized_data(raw_msg=raw_msg)
        return msg

    def _read_raw_msg(self):
        try:
            bytes = self.port.inWaiting()
        except:
            bytes = 0
        raw_msg = self.port.read(size=bytes)
        return raw_msg

    def _parse_msg(self, raw_msg):
        # TODO: regex way to do this.
        # Note: nmea0183 sentences starts with $ or ! and
        # ends in <CR><LF> (hex:0x0d, dec:13)(hex:0x0d, dec:13)
        parsed_msg = ""
        if len(parsed_msg) < 2:
            return None
        return parsed_msg

    def stop():
        self.uart_pin.cleanup()
