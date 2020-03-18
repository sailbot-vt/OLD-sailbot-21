from src.airmar.airmar_input_thread import AirmarInputThread as Airmar

from src.rc_input.rc_input_thread import RCInputThread as RCInput
from src.rudder.rudder_listener import RudderListener as Rudder
from src.sail.sail_listener import SailListener as Sail

from src.arduino.arduino import Arduino

from src.autonomy.events.fleet_race import FleetRace

from src.boat.boat import Boat
from src.world.world import World

from src.logging.logger import Logger

def main():
    """Runs the program."""

    print("Virginia Tech SailBOT\n\n    \"I wish to have no connection with "
          "any ship that does not sail fast\"\n            - John Paul Jones\n\n\n")

    # State objects
    boat = Boat()
    world = World()

    logger = Logger()

    # Init threads
    airmar = Airmar()
    rc_input = RCInput()
    sail = sail.SailListener(boat, world)
    rudder = rudder.RudderListener()
    arduino = Arduino()

    # Start threads
    airmar.start()
    rc_input.start()
    arduino.start()
    sail.start()
    rudder.start()

    # Prompt for event
    print("Select event:\n"
          "0 -- Fleet Race\n"
          "1 -- Endurance Race\n"
          "2 -- Payload Event\n"
          "3 -- Precision Navigation\n"
          "4 -- Station Keeping\n"
          "5 -- Collision Avoidance\n"
          "6 -- Search\n"
          "7 -- RC Mode\n")

    cmd = input()

    if cmd == 0:
        FleetRace(boat, wind, world)    # run fleet race
    elif cmd == 1:
        pass        # run endurance race
    elif cmd == 2:
        pass        # run payload event
    elif cmd == 3:
        pass        # run precision navigation 
    elif cmd == 4:
        pass        # run station keeping
    elif cmd == 5:
        pass        # run collision avoidance
    elif cmd == 6:
        pass        # run search
    elif cmd == 7:
        pass        # run RC mode


if __name__ == "__main__":
    main()
