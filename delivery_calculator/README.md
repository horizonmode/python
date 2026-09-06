# Delivery calculator

A small Python exercise demonstrating dependency injection (DI), the strategy
pattern, protocols, dataclasses, and method naming conventions.

## Scenario

Calculate a delivery price for a parcel with a weight in kilograms and a
destination postcode:

- Standard delivery costs £2 per kilogram.
- Express delivery costs £5 per kilogram plus £10.
- A shipping service uses the calculator supplied to it, prints the quote, and
  records the price in its history.

For a 3 kg parcel, standard delivery costs **£6** and express delivery costs **£25**.
The destination is stored but does not currently affect the price.

Run from the repository root:

```sh
python3 delivery_calculator/main.py
```

The service prints each quote, and `main.py` also prints the two labelled results.
Each service instance maintains its own history.

## How the pieces fit together

| File | Responsibility |
| --- | --- |
| `parcel.py` | Holds parcel data in a frozen dataclass |
| `calculators/delivery_calculator.py` | Defines the calculator protocol |
| `calculators/standard_delivery.py` | Implements standard pricing |
| `calculators/express_delivery.py` | Implements express pricing |
| `shipping_service.py` | Delegates pricing, prints the result, and records it |
| `main.py` | Creates the objects and demonstrates both options |

## Dependency injection: supplying a dependency

The shipping service receives a calculator through its constructor:

```python
class ShippingService:
    def __init__(self, delivery_calculator: DeliveryCalculator) -> None:
        self.delivery_calculator = delivery_calculator
        self.history = []
```

The caller chooses the concrete dependency:

```python
standard_service = ShippingService(StandardDelivery())
express_service = ShippingService(ExpressDelivery())
```

This is constructor dependency injection. The service does not need to create
its own calculator or know which concrete calculator it received. No DI framework
is required.

DI is useful when a dependency needs to be configurable or replaceable, including
with a fake during tests. It does not require multiple implementations, a
protocol, or an abstract class.

## Strategy pattern: interchangeable behaviour

`StandardDelivery` and `ExpressDelivery` are strategies: they implement the same
operation using different pricing rules. `ShippingService.quote()` delegates to
the chosen strategy:

```python
quote = self.delivery_calculator.calculate_delivery_cost(parcel)
```

DI describes **how the calculator arrives**. Strategy describes **the role the
calculator plays**. This example uses both. Strategies do not have to be switched
while a service is running; selecting one at construction is enough.

## Protocol: an interface without required inheritance

```python
class DeliveryCalculator(Protocol):
    def calculate_delivery_cost(self, parcel: Parcel) -> float: ...
```

This specifies the operation a calculator must support. Both concrete calculators
provide a compatible method, so they satisfy the protocol without inheriting
from `DeliveryCalculator`. This is called structural typing.

The constructor annotation `delivery_calculator: DeliveryCalculator` lets a type
checker check that supplied objects support the interface. Python does not enforce
that annotation at runtime. Passing an incompatible object can still fail when
the service tries to use it.

Choose a protocol when you want a typed interface across interchangeable objects
without requiring a common base class. A small fake can satisfy it too:

```python
class FixedDelivery:
    def calculate_delivery_cost(self, parcel: Parcel) -> float:
        return 12.0

service = ShippingService(FixedDelivery())
```

## When would an abstract class help?

An abstract base class (`ABC`) is useful when you deliberately want an explicit
inheritance hierarchy with required methods, possibly alongside shared behaviour.
For example, calculators might inherit a reusable validation method:

```python
from abc import ABC, abstractmethod

class BaseDeliveryCalculator(ABC):
    def validate(self, parcel: Parcel) -> None:
        if parcel.weight <= 0:
            raise ValueError("Weight must be positive")

    @abstractmethod
    def calculate_delivery_cost(self, parcel: Parcel) -> float:
        ...
```

A concrete subclass must implement the abstract method before it can be
instantiated. It must also call `validate()` if it wants that validation; inheriting
the helper does not automatically run it. ABC machinery does not check method
signature compatibility at runtime.

The current calculators need no shared implementation, so the protocol is a
straightforward choice. An ABC is not required just because several classes have
the same method.

## Dataclass: representing structured data

```python
@dataclass(frozen=True)
class Parcel:
    weight: float
    destination: str
```

`Parcel` represents a value whose fields describe it. A dataclass generates an
initializer, a useful representation, and field-based equality by default.
`frozen=True` prevents normal field reassignment after creation; it does not make
arbitrary nested objects immutable.

Dataclasses do not automatically validate annotated types or reject negative
weights. They can have methods and validation when needed.

Use a dataclass when those generated behaviours suit the object. A regular class
is a natural choice for `ShippingService`, which coordinates work and maintains
history. It could technically be a dataclass, but that is not necessary simply
to save writing a constructor.

## Should there be a Quote class?

Returning a `float` is sufficient while a quote is just a price. The current history
therefore contains prices only.

If callers need to know which parcel and delivery option a price belongs to, a
quote dataclass could hold that information:

```python
@dataclass(frozen=True)
class Quote:
    parcel: Parcel
    delivery_option: str
    cost: float
```

This is a possible extension, not part of the current implementation. The
calculators could continue returning numeric costs, while the service constructs,
returns, and records `Quote` objects. Its return annotation and history would
then change accordingly.

## Underscore conventions

| Form | Meaning | Example |
| --- | --- | --- |
| `name` | Public method or attribute | `quote()` |
| `_name` | Internal-use convention; still accessible externally | `_print_quote()` |
| `__name` | Name mangling to avoid accidental subclass collisions | `__cache` |
| `__name__` | Special names defined by Python | `__init__()` |
| `name_` | Avoid a keyword collision | `class_` |
| `_` | Conventionally an unused variable | `for _ in range(3)` |

For this service:

```python
def quote(self, parcel: Parcel) -> float:       # Public operation
    ...

def _print_quote(self, quote: float) -> None:   # Internal helper
    ...

def _add_to_history(self, quote: float) -> None:  # Internal helper
    ...
```

A single leading underscore communicates intent; it does not enforce privacy.
Two leading underscores trigger name mangling inside a class: `__cache` in
`ShippingService` becomes `_ShippingService__cache`. That also does not provide
true privacy and is usually unnecessary here.

Keep recognised special methods such as `__init__` unchanged. Do not invent
double-ended names such as `__print_quote__`; use `_print_quote` in both the
definition and the call.

## Choosing the tools

- Supply configurable or replaceable dependencies with **DI**.
- Encapsulate alternative algorithms using the **strategy pattern**.
- Describe required operations without required inheritance using a **Protocol**.
- Use an **ABC** when an explicit inheritance family and required methods help.
- Represent structured values using a **dataclass** when its generated behaviour fits.

These choices are complementary. You do not need to use every tool in every design.
