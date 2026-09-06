from dataclasses import dataclass

from fighters import Fighter


@dataclass(frozen=True)
class BattleResult:
    battle_id: str
    winner: Fighter
    loser: Fighter
    rounds: int

    def __post_init__(self) -> None:
        if self.winner == self.loser:
            raise ValueError("Winner and loser must be different fighters")
        if not isinstance(self.rounds, int) or self.rounds <= 0:
            raise ValueError("Rounds must be a positive integer")
