import unittest
try:
    from unittest.mock import MagicMock, patch, PropertyMock
except ImportError:
    from mock import MagicMock, patch, PropertyMock

from pubsub import pub

from src.arduino.arduino import Arduino

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

from time import sleep

import pdb

class ArduinoTests(unittest.TestCase):
    """ Tests the methods in rudder"""
    def setUp(self):
        """ Create Arduino objecti """ 
        self.arduino = Arduino(mock_bbio=Adafruit_BBIO, mock_port=serial)

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

    @patch('src.arduino.arduino.pub', autospec=True)
    def test_run(self, mock_pub):
        """ Tests run method """
        # set up mock port
        mock_port = MagicMock(autospec=True)
        self.arduino.port = mock_port

        # initialize angle
        rudder_angles = [-20, 0, 20, 75]
        sail_angles = [1.5 * val for val in rudder_angles]
        rear_foil_angles = [1.9 * val for val in rudder_angles]
        jib_angles = [0.45 * val for val in rudder_angles]
        sensor_angles = [-0.77 * val for val in rudder_angles]

        # activate arduino thread
        self.arduino.start()

        # send angle info over pubsub
        for rud, sail, rear_foil, jib, sensor in zip(rudder_angles, sail_angles, rear_foil_angles, \
                                                     jib_angles, sensor_angles):
            pub.sendMessage("turn rudder to", rudder_ang = rud)
            pub.sendMessage("turn sail to", sail_ang = sail)
            pub.sendMessage("turn rear foil to", rear_foil_ang = rear_foil)
            pub.sendMessage("turn jib to", jib_ang = jib)
            pub.sendMessage("turn sensor to", sensor_ang = sensor)

            # wait 0.05 s
            sleep(0.05)

            # assert that call to port write was made for every angle (along with delimiter)
            mock_port.write.assert_any_call(str(rud))
            mock_port.write.assert_any_call(str(sail))
            mock_port.write.assert_any_call(str(rear_foil))
            mock_port.write.assert_any_call(str(jib))
            mock_port.write.assert_any_call(str(sensor))
            mock_port.write.assert_any_call('|')
            mock_port.write.assert_any_call('b')

            mock_port.reset_mock()

            # assert that logging message was sent
            mock_pub.sendMessage.assert_called_with('write msg', author=self.arduino.author_name, msg=self.arduino.data)

            mock_pub.reset_mock()

        # quit arduino thread
        self.arduino.disable_controls()
