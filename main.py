import src.rc_input.rc_input_thread as rc
import src.sail.sail_thread as sail
import src.rudder.rudder_thread as rudder


def main():
    """Runs the program."""
    rc_thread = rc.RCInputThread()
    sail_thread = sail.SailThread()
    rudder_thread = rudder.RudderThread()

    rudder_thread.start()
    sail_thread.start()
    rc_thread.start()

    print("Running")


if __name__ == "__main__":
    main()
