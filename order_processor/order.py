from decimal import Decimal
from threading import Lock
from uuid import uuid4

from order_item import OrderItem
from order_status import OrderStatus


class Order:
    def __init__(self, customer_email: str, items: tuple[OrderItem, ...]):
        if not isinstance(customer_email, str) or not customer_email.strip():
            raise ValueError("customer_email cannot be empty")
        if not isinstance(items, tuple) or not items:
            raise ValueError("items must be a non-empty tuple")
        if not all(isinstance(item, OrderItem) for item in items):
            raise TypeError("every item must be an OrderItem")

        self.__order_id = uuid4().hex[:12].upper()
        self.__customer_email = customer_email.strip()
        self.__items = items
        self.__status = OrderStatus.PENDING
        self.__payment_transaction_id: str | None = None
        self.__failure_reason: str | None = None
        self.__lock = Lock()

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def customer_email(self) -> str:
        return self.__customer_email

    @property
    def items(self) -> tuple[OrderItem, ...]:
        return self.__items

    @property
    def total(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal("0.00"))

    @property
    def status(self) -> OrderStatus:
        with self.__lock:
            return self.__status

    @property
    def payment_transaction_id(self) -> str | None:
        with self.__lock:
            return self.__payment_transaction_id

    @property
    def failure_reason(self) -> str | None:
        with self.__lock:
            return self.__failure_reason

    def update_status(self, new_status: OrderStatus) -> None:
        if not isinstance(new_status, OrderStatus):
            raise TypeError("new_status must be an OrderStatus")
        with self.__lock:
            self.__status = new_status

    def mark_paid(self, transaction_id: str) -> None:
        if not transaction_id:
            raise ValueError("transaction_id cannot be empty")
        with self.__lock:
            self.__payment_transaction_id = transaction_id
            self.__status = OrderStatus.PAID

    def mark_failed(self, reason: str) -> None:
        with self.__lock:
            self.__failure_reason = reason
            self.__status = OrderStatus.FAILED

    def __str__(self) -> str:
        return (
            f"Order({self.order_id}, total=£{self.total:.2f}, "
            f"status={self.status.value})"
        )
