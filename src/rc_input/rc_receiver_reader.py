from threading import Thread


class RCReader(Thread):
    def __init__(self):
        """Constructs a new RCReader thread."""
        self.name = "rc_reader_thread"  # Easier debugging

    def run(self):
        """Runs the RCReader thread."""
        pass

    def read_input(self):
        """Reads input from the RC receiver.

        Called at fixed, very short time intervals, so it must be fast so it doesn't become backlogged."""
        pass
