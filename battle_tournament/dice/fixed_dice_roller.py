class FixedDiceRoller:
    def __init__(self, rolls: list[int]):
        self.rolls = iter(rolls)

    def roll(self, sides: int) -> int:
        result = next(self.rolls)
        if not 1 <= result <= sides:
            raise ValueError(f"Fixed roll {result} is invalid for a d{sides}")
        return result
