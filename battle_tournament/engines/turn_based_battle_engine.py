from collections.abc import Sequence

from battle_request import BattleRequest
from battle_result import BattleResult
from commentators import Commentator
from delays import BattleDelay
from dice import DiceRoller
from exceptions import BattleLimitReachedError
from fighters import Fighter
from strategies import AttackStrategy


class TurnBasedBattleEngine:
    def __init__(
        self,
        strategies: Sequence[AttackStrategy],
        dice_roller: DiceRoller,
        commentator: Commentator,
        delay: BattleDelay,
        maximum_rounds: int = 100,
    ):
        if not strategies:
            raise ValueError("At least one attack strategy is required")
        if not isinstance(maximum_rounds, int) or maximum_rounds <= 0:
            raise ValueError("maximum_rounds must be a positive integer")

        self.__strategies = tuple(strategies)
        self.__dice_roller = dice_roller
        self.__commentator = commentator
        self.__delay = delay
        self.__maximum_rounds = maximum_rounds

    async def fight(self, battle: BattleRequest) -> BattleResult:
        fighter_one = battle.fighter_one
        fighter_two = battle.fighter_two
        fighter_one_health = fighter_one.health
        fighter_two_health = fighter_two.health

        await self.__commentator.announce(
            f"Battle {battle.battle_id}: {fighter_one.name} vs {fighter_two.name}"
        )

        for round_number in range(1, self.__maximum_rounds + 1):
            await self.__commentator.announce(f"Round {round_number}")

            damage = self.__attack(fighter_one, fighter_two)
            fighter_two_health = max(fighter_two_health - damage, 0)
            await self.__announce_attack(
                fighter_one, fighter_two, damage, fighter_two_health
            )

            if fighter_two_health == 0:
                return await self.__create_result(
                    battle, fighter_one, fighter_two, round_number
                )

            damage = self.__attack(fighter_two, fighter_one)
            fighter_one_health = max(fighter_one_health - damage, 0)
            await self.__announce_attack(
                fighter_two, fighter_one, damage, fighter_one_health
            )

            if fighter_one_health == 0:
                return await self.__create_result(
                    battle, fighter_two, fighter_one, round_number
                )

            await self.__delay.wait()

        raise BattleLimitReachedError(
            f"Battle {battle.battle_id} exceeded {self.__maximum_rounds} rounds"
        )

    def __attack(self, attacker: Fighter, defender: Fighter) -> int:
        strategy_roll = self.__dice_roller.roll(len(self.__strategies))
        strategy = self.__strategies[strategy_roll - 1]
        attack_roll = self.__dice_roller.roll(10)
        damage = strategy.calculate_damage(attacker, defender, attack_roll)
        return max(damage, 0)

    async def __announce_attack(
        self,
        attacker: Fighter,
        defender: Fighter,
        damage: int,
        remaining_health: int,
    ) -> None:
        await self.__commentator.announce(
            f"{attacker.name} hits {defender.name} for {damage}; "
            f"{remaining_health} health remains"
        )

    async def __create_result(
        self,
        battle: BattleRequest,
        winner: Fighter,
        loser: Fighter,
        rounds: int,
    ) -> BattleResult:
        await self.__commentator.announce(f"Winner: {winner.name}")
        return BattleResult(battle.battle_id, winner, loser, rounds)
