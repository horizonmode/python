from threading import Thread
from queue import Queue, ShutDown
from time import sleep

from audit import AuditService


class Printer(Thread):
    def __init__(self, name: str, queue: Queue, audit_service: AuditService) -> None:
        if not name:
            raise ValueError("Printer name must be specified.")
        if not queue:
            raise ValueError("Queue must be specified.")
        super().__init__()
        self.name = name
        self.queue = queue
        self.audit_service = audit_service

    def run(self) -> None:
        try:
            self.print_jobs()
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        print(f"Cleaning up {self.name}")

    def print_jobs(self) -> None:
        while True:
            try:
                job = self.queue.get()
            except ShutDown as e:
                print(f"Shutting down {self.name}")
                return
            try:
                if job is None:
                    return
                print(
                    f"Printing {job.document} ({job.pages} pages) for {job.owner}. From Printer {self.name}"
                )
                self.audit_service.increment_pages_printed(job.pages)
            except Exception as e:
                print(f"Failed to print job: {e}")
            finally:
                self.queue.task_done()
            sleep(2)
