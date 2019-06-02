class Trimmer:
    """Auto-trims the sail"""
    def __init__(self, sail_type, boat, world):
        self.wind = world.wind
        self.boat = boat
