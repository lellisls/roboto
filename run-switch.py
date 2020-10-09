#!/usr/bin/env python3
"""
robot_control_inputs.py
www.bluetin.io
"""

__author__ = "Mark Heywood"
__version__ = "0.1.0"
__license__ = "MIT"

from inputs import get_gamepad
from motor import Motor
import RPi.GPIO as GPIO
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)
# Dictionary of game controller buttons we want to include.
controller_input = {'ABS_HAT0X': 0, 'ABS_HAT0Y': 0, 'ABS_RZ': 0, 'BTN_SOUTH': 0,
                    'BTN_WEST': 0, 'ABS_X': 0, 'ABS_Y': 0, 'ABS_Z': 0, 'ABS_RZ': 0}

pwm1 = 13
p2 = 18
p1 = 17

pwm2 = 12
p3 = 27
p4 = 22

m1 = Motor(p1, p2, pwm1)
m2 = Motor(p3, p4, pwm2)

FW = 1
BW = -1
ST = 0

# -----------------------------------------------------------


def gamepad_update():
    # Code execution stops at the following line until gamepad event occurs.
    events = get_gamepad()
    return_code = None
    for event in events:
        logging.info(f"{event.code}, {event.state}")
        event_test = controller_input.get(event.code, None)
        if event_test != None:
            controller_input[event.code] = event.state
            return_code = event.code
        else:
            return_code = None

    return return_code


# -----------------------------------------------------------
SPEED = 30


def drive_control_dpad():
    # Function to drive robot motors
    DY = controller_input['ABS_HAT0Y']
    DX = controller_input['ABS_HAT0X']
    logging.debug(
        'Drive and Speed --> {} || Steering Angle --> {}' .format(DY, DX))
    speed = speed_1 = speed_2 = SPEED
    if DX != 0 and DY == 0:
        dir1 = DX
        dir2 = -DX
    elif DY != 0 and DX == 0:
        dir1 = -DY
        dir2 = -DY
    elif DX == 0 and DY == 0:
        dir1 = dir2 = 0
    else:
        dir1 = -DY
        dir2 = -DY
        multi1 = 1.2 if DX < 0 else 0.8
        multi2 = 1.2 if DX > 0 else 0.8

        speed_1 *= multi1
        speed_2 *= multi2

    m1.run(speed_1, dir1)
    m2.run(speed_2, dir2)


def drive_control_analog():
    DY = -(min(controller_input['ABS_Y'], 32768) / 32768.0)
    DX = (min(controller_input['ABS_X'], 32768) / 32768.0)

    if abs(DX) < 0.2:
        DX = 0
    if abs(DY) < 0.2:
        DY = 0

    logging.debug(
        'Drive and Speed --> {} || Steering Angle --> {}' .format(DY, DX))

    speed_1 = SPEED * (DY + (1 - DX) * DY)
    speed_2 = SPEED * (DY + (1 - DY) * DX)

    dir1 = DY
    dir2 = DY

    if DX == 0 and DY == 0:
        dir1 = dir2 = 0    
    elif DY == 0:
        dir1 = DX
        dir2 = -DX
        speed_1 = abs(DX) * SPEED
        speed_2 = abs(DX) * SPEED

    logging.debug(speed_1, dir1, speed_2, dir2)
    m1.run(abs(speed_1), dir1)
    m2.run(abs(speed_2), dir2)


def drive_control_speed(control_code):
    global SPEED

    if control_code == 'ABS_Z' and controller_input['ABS_Z'] > 0:
        SPEED = max(0, SPEED - 5)
    elif control_code == 'ABS_RZ' and controller_input['ABS_RZ'] > 0:
        SPEED = min(100, SPEED + 5)
# -----------------------------------------------------------


def main():
    """ Main entry point of the app """
    while 1:
        # Get next controller Input
        control_code = gamepad_update()
        if control_code:
            logging.debug(control_code)

        # Gamepad button filter
        if control_code == 'ABS_HAT0X' or control_code == 'ABS_HAT0Y':
            # Drive and steering
            drive_control_dpad()
        elif control_code == 'ABS_X' or control_code == 'ABS_Y':
            drive_control_analog()
        elif control_code == 'ABS_Z' or control_code == 'ABS_RZ':
            drive_control_speed(control_code)
# -----------------------------------------------------------


if __name__ == "__main__":
    """ This is executed when run from the command line """
    try:
        main()
    finally:
        GPIO.cleanup()
