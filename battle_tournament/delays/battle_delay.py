from typing import Protocol


class BattleDelay(Protocol):
    async def wait(self) -> None: ...
