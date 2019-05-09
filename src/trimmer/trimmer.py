from pubsub import pub


class Trimmer:
    """Auto-trims the sail"""
    def __init__(self, sail_type):
        pub.subscribe(None, "apparent wind")
