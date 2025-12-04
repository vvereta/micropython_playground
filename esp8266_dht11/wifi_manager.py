import uasyncio as asyncio
import network


class WIFI_Manager:
    def __init__(self, config):
        self.config = config
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        print("WIFI: Created")

    def is_connected(self):
        return self.wlan.isconnected()

    async def connect(self):
        if self.is_connected():
            return True

        self.wlan.connect(self.config.SSID, self.config.PASSWORD)

        for _ in range(10):  # 10 * 500ms = 5 sec timeout
            if self.is_connected():
                return True
            await asyncio.sleep_ms(500)

        return False

    async def task(self):
        """Check and reconnect every 10 seconds."""
        while True:
            if not self.is_connected():
                print("WIFI: Disconnected")
                await self.connect()
            else:
                print("WIFI: Connected")
            await asyncio.sleep(10)
