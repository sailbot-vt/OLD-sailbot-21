from src.world.wind import Wind


class World:
    """State object for the current world conditions"""
    def __init__(self):
        """Builds a new world.

        Defaults to large biomes world type. You may spawn in the middle of an ocean. Wave if you see Herobrine.
        """
        self.wind = Wind()
        print("World ready")
