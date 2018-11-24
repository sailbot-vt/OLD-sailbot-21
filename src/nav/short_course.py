from src.utils import *
from src.world import World
from src.boat import Boat


def generate_path(
        start,
        end,
        world,
        boat
):
    """Generates a navigation path from the starting point to the ending point.

    Keyword arguments:
    start -- The start point, a Vec2
    end -- The end point, a Vec2
    world -- A World object holding the current conditions
    boat -- A Boat object holding the boat design specifications

    Returns:
    An array of Vec2s along the routed path
    """
    pass