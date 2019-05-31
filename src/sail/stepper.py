import time
import math
from numpy import sign


def set_all_pins_low(pins):
    for pin in pins:
        pin.set_state(False)


def wavedrive(pins, pin_index):
    for i in range(len(pins)):
        if i == pin_index:
            pins[i].set_state(True)
        else:
            pins[i].set_state(False)


def fullstep(pins, pin_index):
    """pin_index is the lead pin"""
    pins[pin_index].set_state(True)
    pins[(pin_index + 3) % 4].set_state(True)
    pins[(pin_index + 1) % 4].set_state(False)
    pins[(pin_index + 2) % 4].set_state(False)


class StepperTrimmer:
    def __init__(self, pins, center_angle, boat, world):
        self.wind = world.wind
        self.boat = boat
        self.stepper = Stepper(pins)
        self.stepper.rotate(center_angle)
        self.stepper.zero_angle()
        self.centerline_angle = center_angle

    def trim_in_by(self, degrees_in):
        # 1 if on port tack, -1 if on starboard tack
        current_tack = sign(self.wind.angle_relative_to_wind(self.boat.current_heading))
        self.stepper.rotate(-current_tack * degrees_in)


class Stepper:
    def __init__(self, pins, steps_per_rev=2048.0):
        self.pins = pins

        set_all_pins_low(self.pins)

        self.angle = 0
        self.steps_per_rev = steps_per_rev

        # Initialize stepping mode
        self.drivemode = fullstep

    def rotate(self, degrees=360, rpm=15):
        step = 0

        # Calculate time between steps in seconds
        wait_time = 60.0 / (self.steps_per_rev * rpm)

        # Convert degrees to steps
        steps = math.fabs(degrees * self.steps_per_rev / 360.0)
        self.direction = 1

        if degrees < 0:
            self.pins.reverse()
            self.direction = -1

        while step < steps:
            for pin_index in range(len(self.pins)):
                self.drivemode(self.pins, pin_index)
                time.sleep(wait_time)
                step += 1
                self.angle = (self.angle + self.direction / self.steps_per_rev
                              * 360.0) % 360.0

        if degrees < 0:
            self.pins.reverse()

        set_all_pins_low(self.pins)

    def zero_angle(self):
        self.angle = 0
