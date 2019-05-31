import src.airmar.airmar_input_thread as airmar
import src.rc_input.rc_input_thread as rc
import src.rudder.rudder as rudder
import src.sail.sail as sail
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
    sail = sail.Sail()
    rudder = rudder.Rudder()
    captain_thread = captain.Captain(boat, world)

    airmar_thread.start()
    rudder.start()
    sail.start()
    rc_thread.start()
    captain_thread.start()

    while True:
        print("Waiting for input:\nw: drop mark\ns: start navigation\ne: end navigation\n^C: exit program")
        cmd = input()
        if cmd == 'd':
            captain_thread.drop_mark()
        elif cmd == 's':
            captain_thread.enable()
        elif cmd == 'e':
            captain_thread.disable()


if __name__ == "__main__":
    main()
