# Concurrent Order Processor

This scenario expands the single print queue into a three-stage threaded
pipeline. Orders move through payment, fulfilment, and notification queues.

## Architecture

```text
order queue
    ↓
payment workers × 3
    ↓
fulfilment queue
    ↓
fulfilment workers × 2
    ↓
notification queue
    ↓
notification worker
```

## Concepts demonstrated

### Pipeline pattern

Each stage performs one responsibility and passes successful work to the next
queue. A slow stage can be scaled by changing its worker count independently.

### Thread pools and work distribution

Each worker inherits from `Thread`. Multiple workers block on the same queue,
and each queued object is delivered to one available worker.

### Dependency inversion

Workers depend on small protocols:

- `PaymentProcessor`
- `InventoryService`
- `FulfilmentService`
- `NotificationService`

`main.py` selects the concrete implementations and injects them into
`OrderProcessor`. Workers coordinate behavior without knowing how payment,
inventory, fulfilment, or notification are implemented.

### Composition root

`main.py` is the one place where concrete dependencies are assembled. Keeping
construction at the program boundary makes the internal classes easier to test.

### Thread-safe shared state

Inventory uses a lock so checking and decrementing stock form one atomic
operation. A locked set prevents an order ID from being submitted twice.

### Failure handling and rollback

If stock reservation fails partway through an order, earlier reservations are
released. A failed payment also restores stock. An exception from one job does
not terminate its worker thread.

### Graceful lifecycle

`OrderProcessor` starts workers, waits for every pipeline stage, submits one
sentinel per worker, and joins the threads. Its context-manager methods wrap this
lifecycle safely.

### Test doubles

The tests inject fake payment, notification, and fulfilment behavior. This makes
failure paths fast and deterministic without changing production classes.

## Run

```bash
cd /Users/sebsmith/python/order_processor
python3 main.py
```

The demo submits five orders for one keyboard. Exactly one order should complete,
four should fail, and remaining stock should be zero.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The tests cover last-item contention, payment rollback, partial reservation
rollback, and duplicate submissions.

## Concurrency limitation

Threads are effective here because real payment and notification work would be
I/O-bound. CPU-heavy Python calculations generally do not gain the same parallel
speedup because of the GIL.
