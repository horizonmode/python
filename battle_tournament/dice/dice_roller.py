from typing import Protocol


class DiceRoller(Protocol):
    def roll(self, sides: int) -> int: ...
