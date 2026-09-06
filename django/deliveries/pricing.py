from decimal import Decimal
from typing import Protocol


class DeliveryCalculator(Protocol):
    def calculate(self, weight: Decimal) -> Decimal: ...


class StandardDelivery:
    def calculate(self, weight: Decimal) -> Decimal:
        return weight * Decimal("2")


class ExpressDelivery:
    def calculate(self, weight: Decimal) -> Decimal:
        return weight * Decimal("5") + Decimal("10")


class ShippingService:
    def __init__(self, calculator: DeliveryCalculator) -> None:
        self.calculator = calculator

    def quote(self, weight: Decimal) -> Decimal:
        return self.calculator.calculate(weight)


def calculator_for(delivery_type: str) -> DeliveryCalculator:
    calculators = {"standard": StandardDelivery, "express": ExpressDelivery}
    return calculators[delivery_type]()
