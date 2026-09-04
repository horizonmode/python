from tournament import Tournament
from battle_request import Fighter
from typing import Callable
from engines import TurnBasedBattleEngine
from strategies import (
    NormalAttackStrategy,
    AggressiveAttackStrategy,
    DefensiveAttackStrategy,
)
from dice import RandomDiceRoller


def main():
    fighters = [
        Fighter(name="Fighter 1", health=100, attack=10, defence=5),
        Fighter(name="Fighter 2", health=100, attack=12, defence=4),
        Fighter(name="Fighter 3", health=100, attack=8, defence=6),
        Fighter(name="Fighter 4", health=100, attack=11, defence=5),
    ]

    strategies = [
        AggressiveAttackStrategy(),
        DefensiveAttackStrategy(),
        NormalAttackStrategy(),
    ]

    dice_roller = RandomDiceRoller()

    battle_engine = TurnBasedBattleEngine(strategies, dice_roller)
    tournament = Tournament(fighters=fighters, battle_engine=battle_engine)
    winner = tournament.run_tournament()
    print(f"The winner is: {winner.name if winner else 'No winner'}")


if __name__ == "__main__":
    main()
