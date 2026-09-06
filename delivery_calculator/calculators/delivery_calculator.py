from typing import Protocol
from parcel import Parcel


class DeliveryCalculator(Protocol):
    def calculate_delivery_cost(self, parcel: Parcel) -> float: ...
