import random


class RandomDiceRoller:
    def roll(self, sides: int) -> int:
        if not isinstance(sides, int) or sides <= 0:
            raise ValueError("sides must be a positive integer")
        return random.randint(1, sides)
