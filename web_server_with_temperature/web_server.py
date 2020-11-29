import socket

import uasyncio as asyncio


html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266</title> </head>
    <body>
        <h1>Hello!</h1>
    </body>
</html>
"""


def start_server():
    addr = ('0.0.0.0', 80)
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)
    return (addr, s)


async def run_server(addr, sock):
    while True:
        conn, addr = sock.accept()
        print('client connected from', addr)

        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(html)
        conn.close()
        await asyncio.sleep(0)
