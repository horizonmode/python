from fighters import Fighter


class DefensiveAttackStrategy:
    def calculate_damage(self, attacker: Fighter, defender: Fighter, roll: int) -> int:
        if roll == 1:  # 10% chance to miss when rolling a d10
            return 0
        return max(attacker.attack - (defender.defence * 2) + roll, 0)
