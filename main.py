import src.airmar.airmar_input_thread as airmar
import src.rc_input.rc_input_thread as rc
import src.rudder.rudder_listener as rudder
import src.sail.sail_listener as sail
import src.nav.captain as captain

import src.arduino.arduino.Arduino as Arduino

from src.boat.boat import Boat
from src.world.world import World
from src.tracking.map import Map
from src.logging.logger import Logger

from flask_app import create_app, create_socket

def main():
    """Runs the program."""

    print("Virginia Tech SailBOT\n\n    \"I wish to have no connection with "
          "any ship that does not sail fast\"\n            - John Paul Jones\n\n\n")

    # State objects
    boat = Boat()
    world = World()
    
    # Threads
    logger = Logger()
    tracker = Map(boat=boat, toggle_update=True)
    airmar_thread = airmar.AirmarInputThread(logger=logger)
    rc_thread = rc.RCInputThread()
    Sail = sail.SailListener(boat, world)
    Rudder = rudder.RudderListener()
    arduino_thread = Arduino()
    captain_thread = captain.Captain(boat, world)

    tracker.start()
    airmar_thread.start()
    rc_thread.start()
    captain_thread.start()
    arduino_thread.start()

    # Start flask-socketio
    app = create_app()
    socketio = create_socket(app,
        captain=captain_thread, 
        boat=boat, 
        world=world, 
        logger=logger,
        tracker=tracker
    )
    socketio.run(app)


if __name__ == "__main__":
    main()
