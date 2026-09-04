from dataclasses import dataclass


@dataclass(frozen=True)
class Fighter:
    name: str
    health: int
    attack: int
    defence: int
