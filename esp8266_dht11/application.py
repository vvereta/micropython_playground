import uasyncio as asyncio
import urequests
from wifi_manager import WIFI_Manager
from led_manager import LED_Manager
from sensor import Sensor


class Application:
    def __init__(self, config):
        self.config = config

        self.wifi = WIFI_Manager(config)
        self.led = LED_Manager()
        self.sensor = Sensor(config=config, pin_no=4, interval=60)

        # Set callback for sensor data
        self.sensor.set_callback(send_to_adafruit)

    async def start(self):
        asyncio.create_task(self.wifi.task())
        asyncio.create_task(self.led.task())
        asyncio.create_task(self._wifi_monitor())
        asyncio.create_task(self.sensor.task())

        # Keep application alive
        while True:
            await asyncio.sleep(3600)

    async def _wifi_monitor(self):
        """Update LED pattern according to WiFi state."""
        # TODO: Save state
        while True:
            if self.wifi.is_connected():
                # Connected: solid ON
                self.led.set_pattern("solid", True)
            else:
                # Try to detect if connecting (WiFi is busy)
                # If STA is active but not connected → connecting
                if self.wifi.wlan.active():
                    # Connecting: fast blink
                    self.led.set_pattern("blink", 0.2, 0.2)
                else:
                    # Disconnected: slow blink
                    self.led.set_pattern("blink", 1.0, 1.0)

            await asyncio.sleep(1)  # check every second


def send_data(cfg, feed, value, label):
    url = (
        "https://io.adafruit.com/api/v2/"
        f"{cfg.ADAFRUIT_IO_USERNAME}/feeds/{feed}/data"
    )

    headers = {
        "Content-Type": "application/json",
        "X-AIO-Key": cfg.ADAFRUIT_IO_KEY
    }

    try:
        resp = urequests.post(url, headers=headers, data='{"value":%s}' % value)
        print(f"{label}:", resp.status_code)
        resp.close()
    except Exception as e:
        print(f"{label} ERROR:", e)


def send_temp(cfg, temp):
    send_data(cfg, cfg.feed_temp, temp, "TEMP")


def send_hum(cfg, hum):
    send_data(cfg, cfg.feed_hum, hum, "HUM")


def send_to_adafruit(cfg, temp, hum):
    send_temp(cfg, temp)
    send_hum(cfg, hum)
