import network
import socket
import time
import ujson as json

def read_config(config_file='config.json'):
    with open(config_file) as json_file:
        return json.load(json_file)


def do_wifi_connect():
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)

        config = read_config()
        ssid = config['ssid']
        password = config['password']
        sta_if.connect(ssid, password)

        while not sta_if.isconnected():
            time.sleep_ms(500)

    print('network config:', sta_if.ifconfig())
    return sta_if


html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266</title> </head>
    <body>
        <h1>Hello!</h1>
    </body>
</html>
"""


def run_server():
    addr = ('0.0.0.0', 80)
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        conn, addr = s.accept()
        print('client connected from', addr)

        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(html)
        conn.close()


def main():
    sta_if = do_wifi_connect()
    run_server()


if __name__ == '__main__':
    main()
