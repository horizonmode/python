from asyncio import Lock

from battle_result import BattleResult


class InMemoryBattleRepository:
    def __init__(self):
        self.__results: list[BattleResult] = []
        self.__lock = Lock()

    async def save(self, result: BattleResult) -> None:
        if not isinstance(result, BattleResult):
            raise TypeError("result must be a BattleResult")
        async with self.__lock:
            self.__results.append(result)

    async def get_all(self) -> tuple[BattleResult, ...]:
        async with self.__lock:
            return tuple(self.__results)
