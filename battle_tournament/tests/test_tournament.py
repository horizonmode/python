import asyncio
import sys
import unittest
from pathlib import Path

# Allow the standalone project imports to work from any current directory.
PROJECT_DIRECTORY = Path(__file__).resolve().parents[1]
if str(PROJECT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIRECTORY))

from battle_request import BattleRequest
from battle_result import BattleResult
from dice import FixedDiceRoller
from engines import TurnBasedBattleEngine
from exceptions import BattleLimitReachedError
from fighters import Fighter
from repositories import InMemoryBattleRepository
from strategies import NormalAttackStrategy
from tournament import Tournament


class RecordingCommentator:
    def __init__(self):
        self.messages: list[str] = []

    async def announce(self, message: str) -> None:
        self.messages.append(message)


class NoDelay:
    async def wait(self) -> None:
        pass


class SequentialIdGenerator:
    def __init__(self):
        self.next_number = 1

    def new_id(self) -> str:
        battle_id = f"TEST-{self.next_number}"
        self.next_number += 1
        return battle_id


class FirstFighterWinsEngine:
    def __init__(self):
        self.battles: list[BattleRequest] = []
        self.active_battles = 0
        self.maximum_concurrent_battles = 0

    async def fight(self, battle: BattleRequest) -> BattleResult:
        self.battles.append(battle)
        self.active_battles += 1
        self.maximum_concurrent_battles = max(
            self.maximum_concurrent_battles,
            self.active_battles,
        )
        try:
            # Yield control so another arena can start its battle.
            await asyncio.sleep(0.01)
            return BattleResult(
                battle.battle_id,
                battle.fighter_one,
                battle.fighter_two,
                1,
            )
        finally:
            self.active_battles -= 1


class DomainTests(unittest.TestCase):
    def test_fighter_cannot_battle_itself(self) -> None:
        fighter = Fighter("Solo", 10, 2, 1)

        with self.assertRaises(ValueError):
            BattleRequest("B1", fighter, fighter)


class TurnBasedBattleEngineTests(unittest.IsolatedAsyncioTestCase):
    async def test_fixed_dice_produces_a_deterministic_winner(self) -> None:
        hero = Fighter("Hero", health=10, attack=5, defence=0)
        slime = Fighter("Slime", health=5, attack=1, defence=0)
        commentator = RecordingCommentator()
        engine = TurnBasedBattleEngine(
            strategies=(NormalAttackStrategy(),),
            dice_roller=FixedDiceRoller([1, 1]),
            commentator=commentator,
            delay=NoDelay(),
        )

        result = await engine.fight(BattleRequest("B1", hero, slime))

        self.assertEqual(result.winner, hero)
        self.assertEqual(result.loser, slime)
        self.assertEqual(result.rounds, 1)
        self.assertIn("Winner: Hero", commentator.messages)

    async def test_maximum_rounds_prevents_an_infinite_battle(self) -> None:
        fighter_one = Fighter("One", health=10, attack=0, defence=100)
        fighter_two = Fighter("Two", health=10, attack=0, defence=100)
        engine = TurnBasedBattleEngine(
            strategies=(NormalAttackStrategy(),),
            dice_roller=FixedDiceRoller([1, 1] * 4),
            commentator=RecordingCommentator(),
            delay=NoDelay(),
            maximum_rounds=2,
        )

        with self.assertRaises(BattleLimitReachedError):
            await engine.fight(BattleRequest("B1", fighter_one, fighter_two))


class TournamentTests(unittest.IsolatedAsyncioTestCase):
    async def test_tournament_processes_rounds_concurrently(self) -> None:
        original_fighters = [
            Fighter("A", 10, 2, 1),
            Fighter("B", 10, 2, 1),
            Fighter("C", 10, 2, 1),
            Fighter("D", 10, 2, 1),
        ]
        original_copy = list(original_fighters)
        engine = FirstFighterWinsEngine()
        repository = InMemoryBattleRepository()
        commentator = RecordingCommentator()
        tournament = Tournament(
            fighters=original_fighters,
            battle_engine=engine,
            repository=repository,
            id_generator=SequentialIdGenerator(),
            commentator=commentator,
            arena_count=2,
        )

        async with tournament:
            winner = await tournament.run_tournament()

        results = await repository.get_all()
        if winner is None:
            self.fail("Tournament did not produce a winner")
        self.assertEqual(winner.name, "A")
        self.assertEqual(original_fighters, original_copy)
        self.assertEqual(len(engine.battles), 3)
        self.assertEqual(len(results), 3)
        self.assertEqual(engine.maximum_concurrent_battles, 2)
        self.assertEqual(
            {result.battle_id for result in results},
            {"TEST-1", "TEST-2", "TEST-3"},
        )

    async def test_duplicate_battle_ids_are_rejected(self) -> None:
        fighter_one = Fighter("A", 10, 2, 1)
        fighter_two = Fighter("B", 10, 2, 1)
        commentator = RecordingCommentator()
        tournament = Tournament(
            fighters=(),
            battle_engine=FirstFighterWinsEngine(),
            repository=InMemoryBattleRepository(),
            id_generator=SequentialIdGenerator(),
            commentator=commentator,
            arena_count=1,
        )
        battle = BattleRequest("DUPLICATE", fighter_one, fighter_two)

        async with tournament:
            result = await tournament.submit(battle)
            with self.assertRaises(ValueError):
                await tournament.submit(battle)
            await result


if __name__ == "__main__":
    unittest.main()
