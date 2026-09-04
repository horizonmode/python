import random

from fighters import Fighter


class AggressiveAttackStrategy:
    def calculate_damage(self, attacker: Fighter, defender: Fighter, roll: int) -> int:
        misses = random.random()
        if misses < 0.3:  # 30% chance to miss
            print(f"{attacker.name} missed the attack on {defender.name}!")
            return 0
        extra = random.uniform(0, roll)
        return int(((attacker.attack * 2) - defender.defence) + extra)
