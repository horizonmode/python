from asyncio import Future
from dataclasses import dataclass

from battle_request import BattleRequest
from battle_result import BattleResult


@dataclass(frozen=True)
class BattleJob:
    battle: BattleRequest
    result: Future[BattleResult]
