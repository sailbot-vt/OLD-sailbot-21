import time

def time_in_millis():
    """Returns current time in milliseconds"""

    return int(round(time.time() * 1000))
