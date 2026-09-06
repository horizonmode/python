# Async Monster Battle Tournament

This scenario combines object-oriented design patterns, dependency injection,
and asynchronous queue workers. Several arenas can run independent battles in
the same tournament round concurrently.

## Architecture

```text
Tournament
    │ submits BattleJob
    ▼
asyncio.Queue
    ├── ArenaWorker task 1 ──► BattleEngine ──► BattleRepository
    └── ArenaWorker task 2 ──► BattleEngine ──► BattleRepository
              │
              └── completes an asyncio.Future with the result
```

The next bracket round cannot begin until the current round's winners are known,
but all independent battles within a round can overlap.

## Concepts demonstrated

### Async producer-consumer pattern

`Tournament.submit()` places `BattleJob` objects into an `asyncio.Queue`.
`ArenaWorker.run()` awaits work without blocking the event-loop thread.

### Tasks rather than threads

Arena workers are started with `asyncio.create_task()`. Cooperative concurrency
occurs when a worker reaches `await`, such as the simulated battle delay,
repository access, or commentary output.

### Futures for request results

Each `BattleJob` contains an `asyncio.Future`. The submitting tournament awaits
that future while an arena worker completes it with either a `BattleResult` or an
exception.

### Strategy pattern

`AttackStrategy` defines damage calculation. Normal, aggressive, and defensive
strategies implement different algorithms and can be added without changing the
battle engine.

### Repository pattern

`BattleRepository` separates result storage from tournament rules. The current
implementation stores results in memory and protects them with `asyncio.Lock`.

### Dependency injection and protocols

The engine and tournament receive these abstractions:

- `DiceRoller`
- `AttackStrategy`
- `Commentator`
- `BattleDelay`
- `BattleEngine`
- `BattleRepository`
- `BattleIdGenerator`

`main.py` is the composition root that selects concrete implementations.

### Deterministic randomness

Production uses `RandomDiceRoller`; tests inject `FixedDiceRoller`. No battle
logic calls global randomness directly, so tests can predict attacks and winners.

### Async context management and shutdown

`async with tournament` starts worker tasks and guarantees shutdown. Python
3.13's `asyncio.Queue.shutdown()` broadcasts the end of work, workers catch
`QueueShutDown`, and `asyncio.gather()` waits for all arena tasks to exit.

### Async unit testing

Tests use `unittest.IsolatedAsyncioTestCase`. Fakes replace delays, commentary,
ID generation, and the battle engine. One test records the number of active
battles and proves that two first-round matches overlap.

## Run

```bash
cd /Users/sebsmith/python/battle_tournament
python3 main.py
```

## Test

```bash
python3 -m unittest discover -s tests -v
```

## Useful files

- `tournament.py` — queue ownership, bracket coordination, futures, and shutdown
- `workers/arena_worker.py` — async queue consumer
- `engines/turn_based_battle_engine.py` — combat algorithm
- `strategies/` — interchangeable damage strategies
- `repositories/` — result-storage abstraction and implementation
- `tests/test_tournament.py` — deterministic async tests and concurrency proof

## Why some methods remain synchronous

Dice rolls and damage calculations are immediate CPU-local operations, so making
them async would add ceremony without allowing other work to proceed. Operations
that can wait—worker queues, delays, commentary, and repositories—use `async`.
