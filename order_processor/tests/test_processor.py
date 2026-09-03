import unittest
from decimal import Decimal

from exceptions import DuplicateOrderError
from inventory import Inventory
from order import Order
from order_item import OrderItem
from order_status import OrderStatus
from payment import FakePaymentProcessor
from processor import OrderProcessor
from product import Product


class RecordingNotificationService:
    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def send(self, recipient: str, message: str) -> None:
        self.messages.append((recipient, message))


class InstantFulfilmentService:
    def fulfil(self, order: Order) -> None:
        pass


class OrderProcessorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = Inventory()
        self.keyboard = Product("P001", "Keyboard", Decimal("79.99"))
        self.inventory.add_stock(self.keyboard, 1)
        self.notifications = RecordingNotificationService()

    def make_order(self, *items: OrderItem) -> Order:
        return Order("customer@example.com", tuple(items))

    def make_processor(self, payment_processor=None) -> OrderProcessor:
        return OrderProcessor(
            self.inventory,
            payment_processor or FakePaymentProcessor(),
            InstantFulfilmentService(),
            self.notifications,
            payment_workers=2,
            fulfilment_workers=1,
            notification_workers=1,
        )

    def test_only_one_order_can_buy_the_last_item(self) -> None:
        orders = [
            self.make_order(OrderItem("P001", 1, Decimal("79.99")))
            for _ in range(5)
        ]

        with self.make_processor() as processor:
            for order in orders:
                processor.submit(order)

        statuses = [order.status for order in orders]
        self.assertEqual(statuses.count(OrderStatus.COMPLETED), 1)
        self.assertEqual(statuses.count(OrderStatus.FAILED), 4)
        self.assertEqual(self.inventory.get_stock("P001"), 0)

    def test_payment_failure_restores_stock(self) -> None:
        payment = FakePaymentProcessor(
            should_fail=lambda order_id, amount: True
        )
        order = self.make_order(OrderItem("P001", 1, Decimal("79.99")))

        with self.make_processor(payment) as processor:
            processor.submit(order)

        self.assertIs(order.status, OrderStatus.FAILED)
        self.assertEqual(self.inventory.get_stock("P001"), 1)

    def test_partial_reservation_is_rolled_back(self) -> None:
        order = self.make_order(
            OrderItem("P001", 1, Decimal("79.99")),
            OrderItem("MISSING", 1, Decimal("10.00")),
        )

        with self.make_processor() as processor:
            processor.submit(order)

        self.assertIs(order.status, OrderStatus.FAILED)
        self.assertEqual(self.inventory.get_stock("P001"), 1)

    def test_duplicate_order_is_rejected(self) -> None:
        order = self.make_order(OrderItem("P001", 1, Decimal("79.99")))

        with self.make_processor() as processor:
            processor.submit(order)
            with self.assertRaises(DuplicateOrderError):
                processor.submit(order)


if __name__ == "__main__":
    unittest.main()
