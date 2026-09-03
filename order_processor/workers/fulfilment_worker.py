from queue import Queue
from threading import Thread

from fulfilment_service import FulfilmentService
from notification_job import NotificationJob
from order import Order
from order_status import OrderStatus


class FulfilmentWorker(Thread):
    def __init__(
        self,
        fulfilment_queue: Queue,
        notification_queue: Queue,
        fulfilment_service: FulfilmentService,
        *,
        name: str,
    ):
        super().__init__(name=name)
        self.__fulfilment_queue = fulfilment_queue
        self.__notification_queue = notification_queue
        self.__fulfilment_service = fulfilment_service

    def run(self) -> None:
        while True:
            order = self.__fulfilment_queue.get()
            try:
                if order is None:
                    return
                self.__process(order)
            except Exception as error:
                if isinstance(order, Order):
                    order.mark_failed(f"Fulfilment failed: {error}")
            finally:
                self.__fulfilment_queue.task_done()

    def __process(self, order: Order) -> None:
        order.update_status(OrderStatus.FULFILLING)
        self.__fulfilment_service.fulfil(order)
        order.update_status(OrderStatus.COMPLETED)
        self.__notification_queue.put(
            NotificationJob(
                order.customer_email,
                f"Order {order.order_id} is complete.",
            )
        )
