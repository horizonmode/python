# Threaded Print Queue

This scenario runs several printer threads against one shared work queue. It is
the smallest example in the workspace that demonstrates concurrency.

## Architecture

```text
Main thread
    │ puts PrintJob objects
    ▼
queue.Queue
    ├── Printer1 thread
    └── Printer2 thread
```

## Concepts demonstrated

### Producer-consumer pattern

`main.py` produces `PrintJob` objects. Each `Printer` is a consumer that blocks
on `queue.get()` until work is available.

### Starting a thread

`Printer` inherits from `threading.Thread`. Calling `start()` creates a new
thread and invokes its `run()` method there. Calling `run()` directly would just
block the main thread like an ordinary method call.

### Thread-safe queue

`queue.Queue` supplies its own synchronization, so callers do not add another
lock around `put()` or `get()`. Every retrieved job receives one matching
`task_done()`, allowing `queue.join()` to wait for completion.

### Broadcast shutdown

Python 3.13's `Queue.shutdown()` prevents new submissions and wakes printers
blocked on `get()`. Each printer catches `queue.ShutDown`, leaves its processing
loop, and performs cleanup.

### Guaranteed cleanup

The worker's outer `try/finally` guarantees that `cleanup()` executes whenever
the printer exits normally or unexpectedly.

### Shared state and locks

Both printers update one audit counter. `PrinterAudit` protects that shared
mutable value with `threading.Lock`. The queue itself does not require an
additional lock.

### Dependency injection with a protocol

`Printer` receives an `AuditService` rather than constructing `PrinterAudit`.
Another audit implementation could therefore be supplied without changing the
printer.

## Files

- `print_job.py` — printable job data
- `printer.py` — threaded queue consumer and cleanup
- `audit/audit_service.py` — audit protocol
- `audit/printer_audit.py` — thread-safe in-memory audit implementation
- `main.py` — queue creation, worker startup, shutdown, and joining

## Run

```bash
cd /Users/sebsmith/python/print_queue
python3 main.py
```

## Important distinction

`queue.join()` waits for queue accounting to reach zero. `printer.join()` waits
for a thread to terminate. They solve different problems, and a clean shutdown
uses both.
