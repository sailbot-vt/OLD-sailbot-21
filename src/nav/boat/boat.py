class Boat:
    """Contains data about the capabilities of the boat."""

    @property
    def max_heel_angle(self):
        return 0

    def get_velocity(self, heading, world, t):
        """Estimates the velocity of the boat.

        Keyword arguments:
        heading -- The GPS heading of the boat
        world -- The world environment to use in estimating the velocity
        t -- The time at which the velocity will be estimated
        """
        return 1

    def polar_speed(self, apparent_wind):
        pass


class MockBoat(Boat):
    """Provides a simplified Boat for testing"""
    def get_velocity(self, heading, world, t):
        pass