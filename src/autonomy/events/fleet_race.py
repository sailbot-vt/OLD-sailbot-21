from src.autonomy.objectives import Objectives
from src.autonomy.events.base_event import Event
from src.autonomy.events.config_reader import read_interval

class FleetRace(Event):
    """Fleet race event"""
    def __init__(self, tracker, boat, wind):
        """
        Initializes fleet race event
        """
        super().__init__(tracker, boat, wind)

    def read_interval(self):
        """
        Reads update interval from config
        Side Effects:
            update_interval -- sets attribute update_interval using config
        """
        self.update_interval = read_interval('fleet_race')

    def create_objectives(self):
        """
        Returns objectives based on enumeration file
        """
        self.objectives = [Objectives.ENTER_STARTING_GATE, Objectives.ROUND_BUOYS_CCW, Objectives.ENTER_STARTING_GATE]
