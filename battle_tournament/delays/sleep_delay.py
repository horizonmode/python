from asyncio import sleep


class SleepDelay:
    def __init__(self, seconds: float):
        if seconds < 0:
            raise ValueError("Delay cannot be negative")
        self.seconds = seconds

    async def wait(self) -> None:
        await sleep(self.seconds)
