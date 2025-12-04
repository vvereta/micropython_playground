import uasyncio as asyncio
from config import Config
from application import Application


def handle_exception(loop, context):
    print("Unhandled exception:", context["message"])


async def main():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

    cfg = Config()
    app = Application(cfg)
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
