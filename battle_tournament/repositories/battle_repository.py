from typing import Protocol

from battle_result import BattleResult


class BattleRepository(Protocol):
    async def save(self, result: BattleResult) -> None: ...

    async def get_all(self) -> tuple[BattleResult, ...]: ...
