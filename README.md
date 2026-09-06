# Python OOP, Concurrency, and Data Science Scenarios

This workspace contains seven small programs covering object-oriented programming,
dependency injection, threaded and asynchronous worker systems, and data analysis.

## Requirements

- Python 3.13 or newer
- The delivery data analysis uses pandas, Matplotlib, NumPy, and SciPy.
- The other scenarios use only the standard library.

Python 3.13 is required because the print queue and battle tournament use the
queue shutdown APIs introduced in that version.

For the data analysis scenario, run these commands from the repository root.
Skip environment creation if `.venv` already exists:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas matplotlib numpy scipy
```

## Learning path

| Scenario | Main concepts |
| --- | --- |
| [Books](books/README.md) | Classes, objects, methods, class variables, and `__str__` |
| [Bank](bank/README.md) | Inheritance, abstract base classes, encapsulation, exceptions, and dependency injection |
| [Delivery calculator](delivery_calculator/README.md) | Dataclasses, protocols, dependency injection, the Strategy pattern, and underscore conventions |
| [Delivery data analysis](delivery_data_analysis/README.md) | pandas, data validation, object-oriented analysis, descriptive statistics, plots, and Welch's t-test |
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

Replace `books` with `bank`, `delivery_calculator`, `delivery_data_analysis`,
`print_queue`, `order_processor`, or `battle_tournament`. For data analysis, activate
the environment first and use `python main.py`.

You can also run the data analysis directly from the repository root:

```bash
.venv/bin/python delivery_data_analysis/main.py
```

It prints validation and statistical summaries and opens two graphs. The supplied
three-row dataset has only one express delivery, so the significance test reports
insufficient observations. See its README for interpretation and limitations.

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

The delivery calculator focuses on interchangeable pricing strategies and data
objects. The delivery data analysis applies object-oriented organisation to a
DataFrame, builds statistical summaries and plots, and introduces hypothesis
testing with an explicit result dataclass.

A recurring design rule is that high-level coordination code should receive its
dependencies rather than constructing them internally. This makes behavior
replaceable and allows tests to inject fast, deterministic fakes.
