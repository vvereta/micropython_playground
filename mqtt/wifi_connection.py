import network
import time
import utils


def do_wifi_connect():
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)

        config = utils.read_config()
        ssid = config['ssid']
        password = config['password']
        sta_if.connect(ssid, password)

        while not sta_if.isconnected():
            time.sleep_ms(500)

    print('network config:', sta_if.ifconfig())
    return sta_if
