import random

from fighters import Fighter


class DefensiveAttackStrategy:
    def calculate_damage(self, attacker: Fighter, defender: Fighter, roll: int) -> int:
        misses = random.random()
        if misses < 0.1:  # 10% chance to miss
            print(f"{attacker.name} missed the attack on {defender.name}!")
            return 0
        extra = random.uniform(0, roll)
        return int((attacker.attack - (defender.defence * 2)) + extra)
