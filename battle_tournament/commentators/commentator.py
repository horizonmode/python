from typing import Protocol


class Commentator(Protocol):
    async def announce(self, message: str) -> None: ...
