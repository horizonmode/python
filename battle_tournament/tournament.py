from battle_request import BattleRequest, Fighter
from typing import List
import random


class Tournament:
    def __init__(self, fighters: List[Fighter], battle_engine):
        self.fighters = fighters
        self.battle_engine = battle_engine

    def run_tournament(self) -> Fighter | None:
        while len(self.fighters) > 1:
            fighter1 = self.fighters.pop(0)
            fighter2 = self.fighters.pop(0)
            battle_request = BattleRequest(
                battle_id=f"{random.randint(1, 1000)}",
                fighter_one=fighter1,
                fighter_two=fighter2,
            )
            result = self.battle_engine.fight(battle_request)
            winner = result.winner
            self.fighters.append(winner)

        return self.fighters[0] if self.fighters else None
