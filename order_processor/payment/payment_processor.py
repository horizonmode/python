from typing import Protocol
from decimal import Decimal


class PaymentProcessor(Protocol):
    def pay(self, order_id: str, amount: Decimal) -> str: ...
