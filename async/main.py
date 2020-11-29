import uasyncio as asyncio

async def bar():
    count = 0
    while True:
        count += 1
        print(count)
        await asyncio.sleep(1)

async def foo():
    word = ""
    while True:
        word += "z"
        print(word)
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.create_task(bar())
loop.create_task(foo())
loop.run_forever()
