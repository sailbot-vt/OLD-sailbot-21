import Adafruit_BBIO.UART as uart

from pubsub import pub
from threading import Thread, Lock
import time

class Arduino(Thread):
    """ Provides an interface to arudino connected over UART """

    def __init__(self):
        """
        Set up UART pin
        """
        super().__init__()
        self.is_active = True
        """
        set up UART pin, get baud rate from config
        """
        self.update_interval = 0.01            # hard coded for now, set based on baud rate
        # initialize data to send
        self.data = {"rudder_ang": 0,
                     "sail_ang": 0,
                     "rear_foil_ang": 0,
                     "jib_ang": 0,
                     "sensor_ang": 0}

        # subscribe update functions to their respective pubsub channels
        pub.subscribe(self.update_rudder_ang, "turn rudder to")
        pub.subscribe(self.update_sail_ang, "turn sail to")
        pub.subscribe(self.update_rear_foil_ang, "turn rear foil to")
        pub.subscribe(self.update_jib_ang, "turn jib to")
        pub.subscribe(self.update_sensor_ang, "turn sensor to")
        

    def run(self):
        """ Runs the arduino comms thread """
        print("Started arduino thread")
        while self.is_active:
            for val in self.data.values():
                pass            # send over UART
            print(time.time())
            time.sleep(self.update_interval)

    def update_rudder_ang(self, rudder_ang):
        """ udpates rudder angle from pub sub """
        self.data["rudder_ang"] = rudder_ang
             
    def update_sail_ang(self, sail_ang):
        """ udpates sail angle from pub sub """
        self.data["sail_ang"] = sail_ang

    def update_rear_foil_ang(self, rear_foil_ang):
        """ udpates rear foil angle from pub sub """
        self.data["rear_foil_ang"] = rear_foil_ang 
             
    def update_jib_ang(self, jib_ang):
        """ udpates jib angle from pub sub """
        self.data["jib_ang"] = jib_ang

    def update_sensor_ang(self, sensor_ang):
        """ udpates sensor angle from pub sub """
        self.data["sensor_ang"] = sensor_ang

    def disable_controls(self):
        """ disables arduino comms"""
        self.is_active = False

    def enable_controls(self):
        """ enables arduino comms"""
        self.is_active = True
