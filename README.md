# Python OOP, Dependency Injection, and Concurrency Scenarios

This workspace contains five small programs that build progressively from basic
object-oriented programming to threaded and asynchronous worker systems.

## Requirements

- Python 3.13 or newer
- No third-party packages

Python 3.13 is required because the print queue and battle tournament use the
queue shutdown APIs introduced in that version.

## Learning path

| Scenario | Main concepts |
| --- | --- |
| [Books](books/README.md) | Classes, objects, methods, class variables, and `__str__` |
| [Bank](bank/README.md) | Inheritance, abstract base classes, encapsulation, exceptions, and dependency injection |
| [Print queue](print_queue/README.md) | Threads, a shared queue, locks, worker cleanup, and broadcast shutdown |
| [Order processor](order_processor/README.md) | A multi-stage threaded pipeline, protocols, rollback, and unit testing |
| [Battle tournament](battle_tournament/README.md) | Async queues, worker tasks, futures, Strategy and Repository patterns, and async testing |

The examples are deliberately separate. Run a scenario from its own directory
so its standalone imports resolve correctly.

## Running the scenarios

```bash
cd books
python3 main.py
```

Replace `books` with `bank`, `print_queue`, `order_processor`, or
`battle_tournament`.

## Running tests

The two larger scenarios include unit tests:

```bash
cd order_processor
python3 -m unittest discover -s tests -v
```

```bash
cd battle_tournament
python3 -m unittest discover -s tests -v
```

## How the concepts progress

The books example begins with objects that own state and behavior. The bank adds
inheritance and an abstract contract. The print queue introduces concurrent
workers and shared state. The order processor separates a threaded workflow into
stages and injects its external behaviors. Finally, the battle tournament uses
the same dependency-inversion ideas with `asyncio` tasks and an async queue.

A recurring design rule is that high-level coordination code should receive its
dependencies rather than constructing them internally. This makes behavior
replaceable and allows tests to inject fast, deterministic fakes.
