from fighters import Fighter


class AggressiveAttackStrategy:
    def calculate_damage(self, attacker: Fighter, defender: Fighter, roll: int) -> int:
        if roll <= 3:  # 30% chance to miss when rolling a d10
            return 0
        return max((attacker.attack * 2) - defender.defence + roll, 0)
