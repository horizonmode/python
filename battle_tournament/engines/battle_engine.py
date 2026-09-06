from typing import Protocol

from battle_result import BattleResult
from battle_request import BattleRequest


class BattleEngine(Protocol):
    async def fight(self, battle: BattleRequest) -> BattleResult: ...
