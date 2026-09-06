from fighters import Fighter


class NormalAttackStrategy:
    def calculate_damage(self, attacker: Fighter, defender: Fighter, roll: int) -> int:
        return max(attacker.attack - defender.defence + roll, 0)
