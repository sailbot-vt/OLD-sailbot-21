from src.events.base_event import Event

from src.events.config_reader import config_reader

class FleetRace(Event):
    """Fleet race event"""
    def read_interval(self):
        """
        Reads update interval from config
        Side Effects:
            update_interval -- sets attribute update_interval using config
        """
        self.update_interval = config_reader('fleet_race')

    def run(self):
        """
        Runs event thread
        """
        while self.is_active:
            pass                # TODO: for Aditya
