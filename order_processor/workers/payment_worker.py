from queue import Queue
from threading import Thread

from inventory_service import InventoryService
from notification_job import NotificationJob
from order import Order
from order_status import OrderStatus
from payment.payment_processor import PaymentProcessor


class PaymentWorker(Thread):
    def __init__(
        self,
        order_queue: Queue,
        fulfilment_queue: Queue,
        notification_queue: Queue,
        inventory: InventoryService,
        payment_processor: PaymentProcessor,
        *,
        name: str,
    ):
        super().__init__(name=name)
        self.__order_queue = order_queue
        self.__fulfilment_queue = fulfilment_queue
        self.__notification_queue = notification_queue
        self.__inventory = inventory
        self.__payment_processor = payment_processor

    def run(self) -> None:
        while True:
            order = self.__order_queue.get()
            try:
                if order is None:
                    return
                self.__process(order)
            except Exception as error:
                # A bad job must not terminate the worker thread.
                if isinstance(order, Order):
                    order.mark_failed(f"Unexpected worker error: {error}")
            finally:
                self.__order_queue.task_done()

    def __process(self, order: Order) -> None:
        reserved_items = []

        try:
            order.update_status(OrderStatus.PROCESSING_PAYMENT)

            for item in order.items:
                self.__inventory.reserve(item.product_id, item.quantity)
                reserved_items.append(item)

            # The inventory lock is not held while this dependency runs.
            transaction_id = self.__payment_processor.pay(
                order.order_id,
                order.total,
            )
            order.mark_paid(transaction_id)
            self.__fulfilment_queue.put(order)
        except Exception as error:
            for item in reversed(reserved_items):
                self.__inventory.release(item.product_id, item.quantity)

            order.mark_failed(str(error))
            self.__notification_queue.put(
                NotificationJob(
                    order.customer_email,
                    f"Order {order.order_id} failed: {error}",
                )
            )
