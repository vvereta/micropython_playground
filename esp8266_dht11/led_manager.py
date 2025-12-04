import uasyncio as asyncio
from machine import Pin


class LED_Manager:
    def __init__(self, pin_no=2):
        # GPIO2 = D4 onboard LED, active-low
        self.led = Pin(pin_no, Pin.OUT, value=1)  # OFF at boot
        self._task = None
        self._current_pattern = None
        self._current_args = None
        print("LED: Created")

    async def _blink(self, on_time, off_time):
        while True:
            self.led.off()   # ON
            await asyncio.sleep(on_time)
            self.led.on()    # OFF
            await asyncio.sleep(off_time)

    async def _solid(self, state):
        self.led.value(0 if state else 1)
        while True:
            await asyncio.sleep(3600)

    def set_pattern(self, pattern, *args):
        # If the pattern is unchanged → do nothing
        if pattern == self._current_pattern and args == self._current_args:
            return

        # Otherwise, update state
        self._current_pattern = pattern
        self._current_args = args

        # Cancel previous task if running
        if self._task is not None:
            self._task.cancel()
            self._task = None

        # Create new coroutine
        if pattern == "blink":
            coro = self._blink(*args)
        elif pattern == "solid":
            coro = self._solid(*args)
        else:
            raise ValueError("Unknown pattern")

        # Start new pattern task
        self._task = asyncio.create_task(coro)

    async def task(self):
        """Default blink while app starts."""
        self.set_pattern("blink", 0.1, 0.1)
        while True:
            await asyncio.sleep(3600)
