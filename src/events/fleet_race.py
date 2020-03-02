from autonomy.objectives import Objectives
from src.events.base_event import Event
from src.events.config_reader import read_interval
import src.autonomy.nav.cap as captain


class FleetRace(Event):
    """Fleet race event"""

    def __init__(self, boat, wind, world):
        self.objectives = self.create_objectives()
        self.boat = boat
        self.wind = wind
        self.captain_thread = captain.Captain(boat, world)
        self.captain_thread.start()

    def read_interval(self):
        """
        Reads update interval from config
        Side Effects:
            update_interval -- sets attribute update_interval using config
        """
        self.update_interval = read_interval('fleet_race')

    def run(self):
        """
        Runs event thread
        """
        while self.is_active:
            pass

    def create_objectives(self):
        return [Objectives.ENTER_STARTING_GATE, Objectives.ROUND_BUOYS_CCW, Objectives.RETURN_TO_STARTING_GATE]

