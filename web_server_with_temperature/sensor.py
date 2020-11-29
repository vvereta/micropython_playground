import time
import uasyncio as asyncio

from machine import Pin, I2C


class SI7021:
    "I2C Humidity and Temperature Sensor"
    addr = 0x40
    command_t = bytearray([0xF3])
    command_h = bytearray([0xF5])

    def __init__(self, *, scl=5, sda=4):
        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        self.temperature = 0
        self.humidity = 0

    def write(self, command):
        "Send command to a sensor"
        self.i2c.writeto(self.addr, self.command_t)
        time.sleep(0.2)

    def read(self):
        "Read data from a sensor"
        data = int.from_bytes(self.i2c.readfrom(self.addr, 1), 'big')
        result = data * 256 + data
        return result

    def get_temperature(self):
        "Read temperature from a sensor"
        self.write(self.command_t)
        data = self.read()
        cels_temp = (data * 175.72 / 65536.0) - 46.85
        self.temperature = cels_temp

        return cels_temp

    def get_humidity(self):
        "Get humidity from a sensor"
        self.write(self.command_h)
        data = self.read()
        humidity = (data * 125 / 65536.0) - 6
        self.humidity = humidity

        return humidity

    async def get_temperature_and_humidity(self):
        while True:
            self.get_temperature()
            self.get_humidity()
            print(self.temperature, self.humidity)
            await asyncio.sleep(3)
