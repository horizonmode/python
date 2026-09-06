import asyncio

from commentators import ConsoleCommentator
from delays import SleepDelay
from dice import RandomDiceRoller
from engines import TurnBasedBattleEngine
from fighters import Fighter
from identifiers import UuidBattleIdGenerator
from repositories import InMemoryBattleRepository
from strategies import (
    AggressiveAttackStrategy,
    DefensiveAttackStrategy,
    NormalAttackStrategy,
)
from tournament import Tournament


async def main() -> None:
    fighters = [
        Fighter("Dragon", health=80, attack=15, defence=6),
        Fighter("Wizard", health=60, attack=20, defence=3),
        Fighter("Goblin", health=55, attack=12, defence=4),
        Fighter("Knight", health=75, attack=14, defence=8),
    ]

    repository = InMemoryBattleRepository()
    commentator = ConsoleCommentator()
    engine = TurnBasedBattleEngine(
        strategies=(
            NormalAttackStrategy(),
            AggressiveAttackStrategy(),
            DefensiveAttackStrategy(),
        ),
        dice_roller=RandomDiceRoller(),
        commentator=commentator,
        delay=SleepDelay(0.1),
    )
    tournament = Tournament(
        fighters=fighters,
        battle_engine=engine,
        repository=repository,
        id_generator=UuidBattleIdGenerator(),
        commentator=commentator,
        arena_count=2,
    )

    async with tournament:
        winner = await tournament.run_tournament()

    results = await repository.get_all()
    print(f"\nTournament winner: {winner.name if winner else 'No winner'}")
    print(f"Battles completed: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())
