import uasyncio as asyncio
import dht
from machine import Pin


class Sensor:
    def __init__(self, config, pin_no=4, interval=60):
        """
        pin_no: GPIO pin where DHT11 is connected
        interval: seconds between readings
        """
        self.config = config
        self.dht = dht.DHT11(Pin(pin_no))
        self.interval = interval
        self.callback = None
        print("Sensor: Created on pin", pin_no)

    def set_callback(self, callback):
        """Set a coroutine callback to receive sensor data"""
        self.callback = callback

    async def task(self):
        """Async loop to read DHT11 periodically"""
        while True:
            try:
                self.dht.measure()
                await asyncio.sleep_ms(500)
                temp = self.dht.temperature()
                hum = self.dht.humidity()
                print(f"Sensor: Temp={temp}°C Hum={hum}%")

                if self.callback:
                    self.callback(self.config, temp, hum)
            except Exception as e:
                print("Sensor error:", e)

            await asyncio.sleep(self.interval)
