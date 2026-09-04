from dataclasses import dataclass

from fighters import Fighter


@dataclass(frozen=True)
class BattleRequest:
    battle_id: str
    fighter_one: Fighter
    fighter_two: Fighter
