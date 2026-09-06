from calculators import DeliveryCalculator
from parcel import Parcel


class ShippingService:
    def __init__(self, delivery_calculator: DeliveryCalculator) -> None:
        self.delivery_calculator = delivery_calculator
        self.history = []

    def quote(self, parcel: Parcel) -> float:
        quote = self.delivery_calculator.calculate_delivery_cost(parcel)
        self._print_quote(quote)
        self._add_to_history(quote)
        return quote

    def _print_quote(self, quote: float) -> None:
        print(f"Delivery cost: {quote}")

    def _add_to_history(self, quote: float) -> None:
        self.history.append(quote)
