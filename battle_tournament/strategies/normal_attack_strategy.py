import random

from fighters import Fighter


class NormalAttackStrategy:
    def calculate_damage(self, attacker: Fighter, defender: Fighter, roll: int) -> int:
        extra = random.uniform(0, roll)
        return int((attacker.attack - defender.defence) + extra)
