from collections.abc import Callable
from decimal import Decimal
from itertools import count
from threading import Lock

from exceptions import PaymentError


class FakePaymentProcessor:
    def __init__(
        self,
        should_fail: Callable[[str, Decimal], bool] | None = None,
    ):
        self.__should_fail = should_fail or (lambda order_id, amount: False)
        self.__sequence = count(1)
        self.__lock = Lock()

    def pay(self, order_id: str, amount: Decimal) -> str:
        if self.__should_fail(order_id, amount):
            raise PaymentError(f"Payment failed for order {order_id}")

        with self.__lock:
            transaction_number = next(self.__sequence)

        return f"FAKE-{transaction_number:06d}"
