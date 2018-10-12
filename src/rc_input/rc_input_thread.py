from threading import Timer
from functools import partial
from rc_receiver import make_rc_receiver
from rc_broadcasting import make_broadcaster


# Frequency of RC input read in seconds
READ_INTERVAL = 0.1


def run():
    """Runs the RCReader thread."""
    receiver = make_rc_receiver()
    broadcaster = make_broadcaster()
    t = Timer(READ_INTERVAL, partial(update, receiver, broadcaster))  # Freezes the arguments receiver and broadcaster
    t.start()


def update(receiver, broadcaster) -> None:
    """Reads and broadcasts the RC inputs.

    Keyword arguments:
    receiver -- An RCReceiver object to read.
    """
    receiver.read_input()

    broadcaster.change_mode()
    broadcaster.change_trim()
    broadcaster.move_rudder()


