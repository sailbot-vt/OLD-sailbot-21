import src.airmar.airmar_input_thread as airmar
import src.rc_input.rc_input_thread as rc
import src.rudder.rudder_listener as rudder
import src.sail.sail_listener as sail
import src.nav.captain as captain
import src.arduino.arduino.Arduino as Arduino

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

    # Init threads
    airmar_thread = airmar.AirmarInputThread()
    logger = Logger()
    rc_thread = rc.RCInputThread()
    Sail = sail.SailListener(boat, world)
    Rudder = rudder.RudderListener()
    arduino_thread = Arduino()
    captain_thread = captain.Captain(boat, world)

    # Start threads
    airmar_thread.start()
    rc_thread.start()
    captain_thread.start()
    arduino_thread.start()

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
        pass        # run fleet race
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
