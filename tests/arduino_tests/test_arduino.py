import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from pubsub import pub

from src.arduino.arduino import Arduino

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

class ArduinoTests(unittest.TestCase):
    """ Tests the methods in rudder"""
    def setUp(self):
        """ Create Arduino objecti """ 
        self.arduino = Arduino(mock_bbio=Adafruit_BBIO, mock_port=serial)
        self.arduino.disable_controls()

    def test_update_rudder_ang(self):
        """ Tests update_rudder_ang method """
        rudder_angles = [-20, 0, 20, 75]
        for angle in rudder_angles:
            pub.sendMessage("turn rudder to", rudder_ang = angle)
            assert(self.arduino.data["rudder_ang"] == angle)

    def test_update_sail_ang(self):
        """ Tests update_sail_ang method """
        sail_angles = [-20, 0, 20, 75]
        for angle in sail_angles:
            pub.sendMessage("turn sail to", sail_ang = angle)
            assert(self.arduino.data["sail_ang"] == angle)

    def test_update_rear_foil_ang(self):
        """ Tests update_rear_foil_ang method """
        rear_foil_angles = [-20, 0, 20, 75]
        for angle in rear_foil_angles:
            pub.sendMessage("turn rear foil to", rear_foil_ang = angle)
            assert(self.arduino.data["rear_foil_ang"] == angle)

    def test_update_jib_ang(self):
        """ Tests update_jib_ang method """
        jib_angles = [-20, 0, 20, 75]
        for angle in jib_angles:
            pub.sendMessage("turn jib to", jib_ang = angle)
            assert(self.arduino.data["jib_ang"] == angle)

    def test_update_sensor_ang(self):
        """ Tests update_sensor_ang method """
        sensor_angles = [-20, 0, 20, 75]
        for angle in sensor_angles:
            pub.sendMessage("turn sensor to", sensor_ang = angle)
            assert(self.arduino.data["sensor_ang"] == angle)
