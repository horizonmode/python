from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    price: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.product_id, str) or not self.product_id.strip():
            raise ValueError("product_id cannot be empty")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name cannot be empty")

        price = Decimal(str(self.price)).quantize(Decimal("0.01"))
        if price < 0:
            raise ValueError("price cannot be negative")

        object.__setattr__(self, "product_id", self.product_id.strip())
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "price", price)

    def __str__(self) -> str:
        return f"{self.name} ({self.product_id}) - £{self.price:.2f}"
