from decimal import Decimal

from basic_fulfilment_service import BasicFulfilmentService
from inventory import Inventory
from notifications import ConsoleNotificationService
from order import Order
from order_item import OrderItem
from order_status import OrderStatus
from payment import FakePaymentProcessor
from processor import OrderProcessor
from product import Product


def main() -> None:
    keyboard = Product("P001", "Keyboard", Decimal("79.99"))
    inventory = Inventory()
    inventory.add_stock(keyboard, 1)

    orders = [
        Order(
            customer_email=f"customer{number}@example.com",
            items=(OrderItem(keyboard.product_id, 1, keyboard.price),),
        )
        for number in range(5)
    ]

    # These concrete services are injected into the concurrent processor.
    processor = OrderProcessor(
        inventory=inventory,
        payment_processor=FakePaymentProcessor(),
        fulfilment_service=BasicFulfilmentService(),
        notification_service=ConsoleNotificationService(),
        payment_workers=3,
        fulfilment_workers=2,
        notification_workers=1,
    )

    with processor:
        for order in orders:
            processor.submit(order)
        processor.wait_until_finished()

    print("\nResults:")
    for order in orders:
        reason = f" - {order.failure_reason}" if order.failure_reason else ""
        print(f"{order}{reason}")

    completed = sum(order.status is OrderStatus.COMPLETED for order in orders)
    failed = sum(order.status is OrderStatus.FAILED for order in orders)
    print(f"\nCompleted: {completed}")
    print(f"Failed: {failed}")
    print(f"Remaining keyboard stock: {inventory.get_stock('P001')}")


if __name__ == "__main__":
    main()
