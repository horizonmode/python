from typing import Protocol


class InventoryService(Protocol):
    """The inventory operations required by order-processing code."""

    def reserve(self, product_id: str, quantity: int) -> None: ...

    def release(self, product_id: str, quantity: int) -> None: ...

    def get_stock(self, product_id: str) -> int: ...
