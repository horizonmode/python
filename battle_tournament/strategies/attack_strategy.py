from typing import Protocol

from fighters import Fighter


class AttackStrategy(Protocol):
    def calculate_damage(
        self,
        attacker: Fighter,
        defender: Fighter,
        roll: int,
    ) -> int: ...
