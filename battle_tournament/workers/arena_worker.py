from asyncio import Queue, QueueShutDown

from battle_job import BattleJob
from commentators import Commentator
from engines import BattleEngine
from repositories import BattleRepository


class ArenaWorker:
    def __init__(
        self,
        name: str,
        battle_queue: Queue[BattleJob],
        battle_engine: BattleEngine,
        repository: BattleRepository,
        commentator: Commentator,
    ):
        self.__name = name
        self.__battle_queue = battle_queue
        self.__battle_engine = battle_engine
        self.__repository = repository
        self.__commentator = commentator

    async def run(self) -> None:
        await self.__commentator.announce(f"{self.__name} is ready")

        try:
            while True:
                try:
                    job = await self.__battle_queue.get()
                except QueueShutDown:
                    return

                try:
                    await self.__process(job)
                finally:
                    self.__battle_queue.task_done()
        finally:
            await self.__commentator.announce(f"{self.__name} is closed")

    async def __process(self, job: BattleJob) -> None:
        battle = job.battle

        try:
            await self.__commentator.announce(
                f"{self.__name} hosts battle {battle.battle_id}"
            )
            result = await self.__battle_engine.fight(battle)
            await self.__repository.save(result)
        except Exception as error:
            await self.__commentator.announce(
                f"{self.__name}: battle {battle.battle_id} failed: {error}"
            )
            if not job.result.done():
                job.result.set_exception(error)
        else:
            if not job.result.done():
                job.result.set_result(result)
