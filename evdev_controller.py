#!/usr/bin/env python3

from evdev import InputDevice, categorize, ecodes, list_devices
from asyncio import Queue

import asyncio

STICK_MAX = 255


class Event:
    def __init__(self, code, state):
        self.code = code
        self.state = state

    def __repr__(self):
        return str({
            "code": self.code,
            "state": self.state
        })


axis = {
    0: 'ABS_X',
    1: 'ABS_Y',
    2: 'ABS_RX',
    5: 'ABS_RY',
    9: 'ABS_Z',
    10: 'ABS_RZ',
    16: 'ABS_HAT0X',
    17: 'ABS_HAT0Y',
}

button = {

}

q = Queue()


async def get_gamepad():
    return await q.get()


async def run_controller():
    global q
    dev = None
    while True:
        if dev is None:
            devices = list_devices()
            if len(devices) == 0:
                print("Device not found... Trying again in 3s")
                await asyncio.sleep(3)

            dev = InputDevice(devices[0])

        async for event in dev.async_read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                # print(f"EV_KEY {event.code}: {event.value}")
                if event.code in button.keys():
                    await q.put(Event(button[event.code], value))

            elif event.type == ecodes.EV_ABS:
                if event.code in axis.keys():
                    if axis[event.code] in ["ABS_X", "ABS_Y", "ABS_RX", "ABS_RY"]:
                        value = min(event.value, STICK_MAX) * 2 / STICK_MAX - 1.0
                    elif axis[event.code] in ["ABS_HAT0X", "ABS_HAT0Y"]:
                        value = event.value
                    else:
                        value = event.value/STICK_MAX

                    if abs(value) < 0.01:
                        value = 0.0
                    # print(f"EV_ABS {event.code}: {axis[event.code]} {value}")
                    await q.put(Event(axis[event.code], value))


async def debug_consumer():
    while True:
        event = await get_gamepad()
        if event:
            print(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(run_controller(), debug_consumer()))
