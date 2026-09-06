from asyncio import Lock


class ConsoleCommentator:
    def __init__(self) -> None:
        self.__lock = Lock()

    async def announce(self, message: str) -> None:
        # Keep messages from concurrent arenas as complete output lines.
        async with self.__lock:
            print(message)
