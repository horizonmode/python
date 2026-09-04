from time import sleep

from battle_request import BattleRequest
from battle_result import BattleResult
from fighters import Fighter
from strategies import AttackStrategy
from dice import DiceRoller
from typing import List
import random


class TurnBasedBattleEngine:
    def __init__(self, strategies: List[AttackStrategy], dice_roller: DiceRoller):
        self.strategies = strategies
        self.dice_roller = dice_roller

    def fight(self, battle: BattleRequest) -> BattleResult:
        fighter1 = battle.fighter_one
        fighter2 = battle.fighter_two
        fighter1_health = max(fighter1.health, 0)
        fighter2_health = max(fighter2.health, 0)
        rounds = 0
        winner = None
        loser = None

        while fighter1_health > 0 and fighter2_health > 0:
            print(
                f"Round {rounds + 1} begins: {fighter1.name} (Health: {fighter1_health}) vs {fighter2.name} (Health: {fighter2_health})"
            )
            dice_roll = self.dice_roller.roll(6)
            print(f"Dice rolled: {dice_roll}")
            fighter2_health -= self.attack(fighter1, fighter2, dice_roll)
            print(
                f"{fighter1.name} attacks {fighter2.name} for this round. {fighter2.name}'s health is now {fighter2_health}."
            )
            rounds += 1
            if fighter2_health <= 0:
                break
            fighter1_health -= self.attack(fighter2, fighter1, dice_roll)
            print(
                f"{fighter2.name} attacks {fighter1.name} for this round. {fighter1.name}'s health is now {fighter1_health}."
            )
            rounds += 1
            fighter1_health = max(fighter1_health, 0)
            fighter2_health = max(fighter2_health, 0)
            sleep(2)

        loser = fighter1 if fighter1_health <= 0 else fighter2
        winner = fighter1 if loser == fighter2 else fighter2
        return BattleResult(
            winner=winner, rounds=rounds, loser=loser, battle_id=battle.battle_id
        )

    def attack(self, attacker: Fighter, defender: Fighter, roll: int):
        strategy = random.choice(self.strategies)
        damage = strategy.calculate_damage(attacker, defender, roll)
        return max(damage, 0)
