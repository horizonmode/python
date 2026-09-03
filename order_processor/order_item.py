from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrderItem:
    product_id: str
    quantity: int
    unit_price: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.product_id, str) or not self.product_id.strip():
            raise ValueError("product_id cannot be empty")
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError("quantity must be a positive integer")

        price = Decimal(str(self.unit_price)).quantize(Decimal("0.01"))
        if price < 0:
            raise ValueError("unit_price cannot be negative")

        object.__setattr__(self, "product_id", self.product_id.strip())
        object.__setattr__(self, "unit_price", price)

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.quantity
