import src.airmar.airmar_input_thread as airmar
import src.rc_input.rc_input_thread as rc
import src.rudder.rudder_thread as rudder
import src.sail.sail_thread as sail
import src.nav.captain as captain

from src.boat.boat import Boat
from src.world.world import World


def main():
    """Runs the program."""

    # State objects
    boat = Boat()
    world = World()

    # Threads
    airmar_thread = airmar.AirmarInputThread()
    rc_thread = rc.RCInputThread()
    sail_thread = sail.SailThread()
    rudder_thread = rudder.RudderThread()
    captain_thread = captain.Captain(boat, world)

    airmar_thread.start()
    rudder_thread.start()
    sail_thread.start()
    rc_thread.start()
    captain_thread.start()

    while True:
        cmd = input()
        if cmd == 'w':
            captain_thread.drop_mark()


if __name__ == "__main__":
    main()
