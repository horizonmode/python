from typing import Protocol

from order import Order


class FulfilmentService(Protocol):
    """The fulfilment operation required by a fulfilment worker."""

    def fulfil(self, order: Order) -> None: ...
