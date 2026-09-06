from asyncio import Future, Lock, Queue, create_task, gather, get_running_loop
from collections.abc import Sequence

from battle_job import BattleJob
from battle_request import BattleRequest
from battle_result import BattleResult
from commentators import Commentator
from engines import BattleEngine
from fighters import Fighter
from identifiers import BattleIdGenerator
from repositories import BattleRepository
from workers import ArenaWorker


class Tournament:
    def __init__(
        self,
        fighters: Sequence[Fighter],
        battle_engine: BattleEngine,
        repository: BattleRepository,
        id_generator: BattleIdGenerator,
        commentator: Commentator,
        arena_count: int = 2,
    ):
        if not all(isinstance(fighter, Fighter) for fighter in fighters):
            raise TypeError("Every competitor must be a Fighter")
        if not isinstance(arena_count, int) or arena_count <= 0:
            raise ValueError("arena_count must be a positive integer")

        self.__fighters = list(fighters)
        self.__battle_engine = battle_engine
        self.__repository = repository
        self.__id_generator = id_generator
        self.__commentator = commentator
        self.__battle_queue: Queue[BattleJob] = Queue()
        self.__seen_battle_ids: set[str] = set()
        self.__id_lock = Lock()
        self.__workers = [
            ArenaWorker(
                f"Arena {number}",
                self.__battle_queue,
                battle_engine,
                repository,
                commentator,
            )
            for number in range(1, arena_count + 1)
        ]
        self.__worker_tasks = []
        self.__started = False
        self.__closed = False
        self.__has_run = False

    async def start(self) -> None:
        if self.__started or self.__closed:
            raise RuntimeError("Tournament can only be started once")

        self.__worker_tasks = [
            create_task(worker.run(), name=f"arena-worker-{number}")
            for number, worker in enumerate(self.__workers, start=1)
        ]
        self.__started = True

    async def submit(self, battle: BattleRequest) -> Future[BattleResult]:
        if not self.__started or self.__closed:
            raise RuntimeError("Tournament is not running")
        if not isinstance(battle, BattleRequest):
            raise TypeError("battle must be a BattleRequest")

        async with self.__id_lock:
            if battle.battle_id in self.__seen_battle_ids:
                raise ValueError(f"Duplicate battle ID: {battle.battle_id}")
            self.__seen_battle_ids.add(battle.battle_id)

        result = get_running_loop().create_future()
        await self.__battle_queue.put(BattleJob(battle, result))
        return result

    async def run_tournament(self) -> Fighter | None:
        if not self.__started or self.__closed:
            raise RuntimeError("Tournament is not running")
        if self.__has_run:
            raise RuntimeError("Tournament has already been run")
        self.__has_run = True

        current_round = list(self.__fighters)

        while len(current_round) > 1:
            next_round = []
            result_futures = []

            # An unpaired fighter receives a bye into the next round.
            if len(current_round) % 2 == 1:
                next_round.append(current_round.pop())

            for index in range(0, len(current_round), 2):
                battle = BattleRequest(
                    battle_id=self.__id_generator.new_id(),
                    fighter_one=current_round[index],
                    fighter_two=current_round[index + 1],
                )
                result_futures.append(await self.submit(battle))

            try:
                results = await gather(*result_futures)
            finally:
                # Preserve Queue's task accounting even when a battle fails.
                await self.__battle_queue.join()

            next_round.extend(result.winner for result in results)
            current_round = next_round

        return current_round[0] if current_round else None

    async def wait_until_finished(self) -> None:
        if not self.__started:
            raise RuntimeError("Tournament has not been started")
        await self.__battle_queue.join()

    async def shutdown(self) -> None:
        if not self.__started or self.__closed:
            return

        await self.__battle_queue.join()
        self.__battle_queue.shutdown()
        await gather(*self.__worker_tasks)
        self.__closed = True

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exception_type, exception, traceback) -> None:
        await self.shutdown()
