from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    transaction_type: str
    amount: Decimal
    description: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __str__(self) -> str:
        return (
            f"{self.timestamp:%Y-%m-%d %H:%M:%S} | "
            f"{self.transaction_type:<12} | "
            f"£{self.amount:.2f} | {self.description}"
        )
