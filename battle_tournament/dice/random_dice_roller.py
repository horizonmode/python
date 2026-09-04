import random


class RandomDiceRoller:
    def roll(self, sides: int) -> int:
        return random.randint(1, sides)
