import asyncio


async def startup():
    """
    The main application entry point.

    """

    while True:
        await asyncio.sleep(30)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())


if __name__ == "__main__":
    main()
