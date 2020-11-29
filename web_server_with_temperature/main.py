import uasyncio as asyncio

import config
import sensor
import web_server
import wifi


def main():
    my_sensor = sensor.SI7021(scl=5, sda=4)

    cfg = config.read_config('config.json')
    wifi.do_wifi_connect(cfg)

    addr, sock = web_server.start_server()

    loop = asyncio.get_event_loop()
    loop.create_task(web_server.run_server(addr, sock))
    loop.create_task(my_sensor.get_temperature_and_humidity())
    loop.run_forever()


if __name__ == '__main__':
    main()
