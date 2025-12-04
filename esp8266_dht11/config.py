import ujson


class Config:
    def __init__(self):
        with open("config.json") as f:
            data = ujson.load(f)

        self.SSID = data["SSID"]
        self.PASSWORD = data["PASSWORD"]
        self.ADAFRUIT_IO_USERNAME = data["ADAFRUIT_IO_USERNAME"]
        self.ADAFRUIT_IO_KEY = data["ADAFRUIT_IO_KEY"]

        # feed name: "livingroom" / "bedroom" / "kitchen"
        self.FEED = data["FEED"]

        # Feed names under group:  group.feedname
        self.feed_temp = f"{self.FEED}.temp"
        self.feed_hum = f"{self.FEED}.hum"
