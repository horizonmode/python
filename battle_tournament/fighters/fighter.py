from dataclasses import dataclass


@dataclass(frozen=True)
class Fighter:
    name: str
    health: int
    attack: int
    defence: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Fighter name cannot be empty")
        if not isinstance(self.health, int) or self.health <= 0:
            raise ValueError("Health must be a positive integer")
        if not isinstance(self.attack, int) or self.attack < 0:
            raise ValueError("Attack cannot be negative")
        if not isinstance(self.defence, int) or self.defence < 0:
            raise ValueError("Defence cannot be negative")
