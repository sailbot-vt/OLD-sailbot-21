from src.autonomy.objectives import Objectives
from src.autonomy.events.base_event import Event
from src.autonomy.events.config_reader import read_interval
import src.autonomy.nav.captain as captain


class StationKeepingEvent(Event):

    def __init__(self, wind, boat, world):
        super().__init__()
        self.objectives = self.create_objectives()
        self.boat = boat
        self.wind = wind
        self.world = world
        self.captain_thread = captain.Captain(boat, world)
        self.captain_thread.start()

    def read_interval(self):
        """
                Reads update interval from config
                Side Effects:
                    update_interval -- sets attribute update_interval using config
                """
        self.update_interval = read_interval('station_keeping_event')

    def run(self):
        """
        Runs event thread
        """
        while self.is_active:
            pass

    def create_objectives(self):
        """
                Returns objectives based on enumeration file
                """
        return [Objectives.ENTER_SK_BOX, Objectives.STAY_IN_BOX, Objectives.LEAVE_BOX]
