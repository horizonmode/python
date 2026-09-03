from queue import Queue
from threading import Thread

from notifications.notification_service import NotificationService


class NotificationWorker(Thread):
    def __init__(
        self,
        notification_queue: Queue,
        notification_service: NotificationService,
        *,
        name: str,
    ):
        super().__init__(name=name)
        self.__notification_queue = notification_queue
        self.__notification_service = notification_service

    def run(self) -> None:
        while True:
            job = self.__notification_queue.get()
            try:
                if job is None:
                    return
                self.__notification_service.send(job.recipient, job.message)
            except Exception as error:
                # Notification failures do not kill the worker or repeat payment.
                print(f"[{self.name}] Notification failed: {error}")
            finally:
                self.__notification_queue.task_done()
