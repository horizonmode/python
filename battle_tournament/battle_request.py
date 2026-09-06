from dataclasses import dataclass

from fighters import Fighter


@dataclass(frozen=True)
class BattleRequest:
    battle_id: str
    fighter_one: Fighter
    fighter_two: Fighter

    def __post_init__(self) -> None:
        if not isinstance(self.battle_id, str) or not self.battle_id.strip():
            raise ValueError("battle_id cannot be empty")
        if not isinstance(self.fighter_one, Fighter) or not isinstance(
            self.fighter_two, Fighter
        ):
            raise TypeError("Both competitors must be Fighter objects")
        if self.fighter_one == self.fighter_two:
            raise ValueError("A fighter cannot battle itself")
