from queue import Queue
from threading import Lock

from exceptions import DuplicateOrderError
from fulfilment_service import FulfilmentService
from inventory_service import InventoryService
from notifications.notification_service import NotificationService
from order import Order
from payment.payment_processor import PaymentProcessor
from workers.fulfilment_worker import FulfilmentWorker
from workers.notification_worker import NotificationWorker
from workers.payment_worker import PaymentWorker


class OrderProcessor:
    def __init__(
        self,
        inventory: InventoryService,
        payment_processor: PaymentProcessor,
        fulfilment_service: FulfilmentService,
        notification_service: NotificationService,
        payment_workers: int = 3,
        fulfilment_workers: int = 2,
        notification_workers: int = 1,
    ):
        for name, count in (
            ("payment_workers", payment_workers),
            ("fulfilment_workers", fulfilment_workers),
            ("notification_workers", notification_workers),
        ):
            if not isinstance(count, int) or count <= 0:
                raise ValueError(f"{name} must be a positive integer")

        self.__order_queue = Queue()
        self.__fulfilment_queue = Queue()
        self.__notification_queue = Queue()
        self.__submitted_order_ids: set[str] = set()
        self.__submission_lock = Lock()
        self.__started = False
        self.__shut_down = False

        self.__payment_workers = [
            PaymentWorker(
                self.__order_queue,
                self.__fulfilment_queue,
                self.__notification_queue,
                inventory,
                payment_processor,
                name=f"payment-{number}",
            )
            for number in range(1, payment_workers + 1)
        ]
        self.__fulfilment_workers = [
            FulfilmentWorker(
                self.__fulfilment_queue,
                self.__notification_queue,
                fulfilment_service,
                name=f"fulfilment-{number}",
            )
            for number in range(1, fulfilment_workers + 1)
        ]
        self.__notification_workers = [
            NotificationWorker(
                self.__notification_queue,
                notification_service,
                name=f"notification-{number}",
            )
            for number in range(1, notification_workers + 1)
        ]

    def start(self) -> None:
        if self.__started or self.__shut_down:
            raise RuntimeError("OrderProcessor can only be started once")

        for worker in self.__all_workers:
            worker.start()
        self.__started = True

    def submit(self, order: Order) -> None:
        if not self.__started or self.__shut_down:
            raise RuntimeError("OrderProcessor is not running")
        if not isinstance(order, Order):
            raise TypeError("order must be an Order")

        with self.__submission_lock:
            if order.order_id in self.__submitted_order_ids:
                raise DuplicateOrderError(
                    f"Order '{order.order_id}' has already been submitted"
                )
            self.__submitted_order_ids.add(order.order_id)

        self.__order_queue.put(order)

    def wait_until_finished(self) -> None:
        if not self.__started:
            raise RuntimeError("OrderProcessor has not been started")

        # Each stage can enqueue work for the next, so join in pipeline order.
        self.__order_queue.join()
        self.__fulfilment_queue.join()
        self.__notification_queue.join()

    def shutdown(self) -> None:
        if not self.__started or self.__shut_down:
            return

        self.wait_until_finished()

        self.__stop_workers(self.__order_queue, self.__payment_workers)
        self.__stop_workers(
            self.__fulfilment_queue,
            self.__fulfilment_workers,
        )
        self.__stop_workers(
            self.__notification_queue,
            self.__notification_workers,
        )

        self.__shut_down = True

    @property
    def __all_workers(self) -> list:
        return [
            *self.__payment_workers,
            *self.__fulfilment_workers,
            *self.__notification_workers,
        ]

    @staticmethod
    def __stop_workers(queue: Queue, workers: list) -> None:
        for _ in workers:
            queue.put(None)
        queue.join()
        for worker in workers:
            worker.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception, traceback) -> None:
        self.shutdown()
