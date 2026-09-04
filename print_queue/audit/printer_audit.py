from threading import Lock


class PrinterAudit:
    def __init__(self):
        self.pages_printed = 0
        self.lock = Lock()

    def increment_pages_printed(self, pages: int):
        with self.lock:
            self.pages_printed += pages

    def report(self):
        with self.lock:
            print(f"Total printing is {self.pages_printed} pages.")
