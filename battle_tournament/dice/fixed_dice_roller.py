class FixedDiceRoller:
    def __init__(self, rolls: list[int]):
        self.rolls = iter(rolls)

    def roll(self, _: int) -> int:
        return next(self.rolls)
