from queue import Queue

from printer import Printer
from audit import PrinterAudit
from print_job import PrintJob

print_queue = Queue()

audit_service = PrinterAudit()

printers = [
    Printer("Printer1", print_queue, audit_service),
    Printer("Printer2", print_queue, audit_service),
]

for printer in printers:
    printer.start()

print_queue.put(PrintJob("Document1", 5, "Alice"))
print_queue.put(PrintJob("Document2", 3, "Bob"))
print_queue.shutdown()

print_queue.join()

for printer in printers:
    printer.join()

audit_service.report()
