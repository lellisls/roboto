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

# Dictionary of game controller buttons we want to include.
controller_input = {'ABS_HAT0X': 0, 'ABS_HAT0Y': 0, 'ABS_RZ': 0, 'BTN_SOUTH': 0, 'BTN_WEST': 0, 'ABS_X': 0, 'ABS_Y': 0}

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

#-----------------------------------------------------------

def gamepad_update():
    # Code execution stops at the following line until gamepad event occurs.
    events = get_gamepad()
    return_code = None
    for event in events:
        # print(event.code, event.state)
        event_test = controller_input.get(event.code, None)
        if event_test != None:
            controller_input[event.code] = event.state
            return_code = event.code
        else:
            return_code = None

    return return_code

#-----------------------------------------------------------

def drive_control_dpad():
    # Function to drive robot motors
    DY = controller_input['ABS_HAT0Y']
    DX = controller_input['ABS_HAT0X']
    print('Drive and Speed --> {} || Steering Angle --> {}' .format(DY, DX) )
    speed = speed_1 = speed_2 = 35
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
    DY = ( min( controller_input['ABS_Y'], 32768) / 32768.0 )
    DX = ( min( controller_input['ABS_X'], 32768) / 32768.0 )

    print('Drive and Speed --> {} || Steering Angle --> {}' .format(DY, DX) )
    SPEED = 30
    dir1 = -DY if abs(DY) > 0.3 else DX
    dir2 = -DY if abs(DY) > 0.3 else -DX

    speed_1 = min( abs(DY) + abs(DX), 1) * SPEED - DX * SPEED * 0.2
    speed_2 = min( abs(DY) + abs(DX), 1 ) * SPEED + DX * SPEED * 0.2

    print(speed_1, dir1, speed_2, dir2)
    m1.run(speed_1, dir1)
    m2.run(speed_2, dir2)

#-----------------------------------------------------------

def main():
    """ Main entry point of the app """
    while 1:
        # Get next controller Input
        control_code = gamepad_update()
        if control_code:
            print(control_code)

        # Gamepad button filter
        if control_code == 'ABS_HAT0X' or control_code == 'ABS_HAT0Y':
            # Drive and steering
            drive_control_dpad()
        elif control_code == 'ABS_X' or control_code == 'ABS_Y':
            drive_control_analog()

#-----------------------------------------------------------

if __name__ == "__main__":
    """ This is executed when run from the command line """
    try:
        main()
    finally:
        GPIO.cleanup()