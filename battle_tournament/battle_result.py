from dataclasses import dataclass

from fighters import Fighter


@dataclass(frozen=True)
class BattleResult:
    battle_id: str
    winner: Fighter
    loser: Fighter
    rounds: int
