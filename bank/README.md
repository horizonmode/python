# Banking System

This scenario models bank accounts, transactions, transfers, interest, and
overdrafts. It demonstrates a closely related inheritance hierarchy and simple
dependency injection.

## Concepts demonstrated

### Abstract base class

`BankAccount` inherits from `ABC` and declares `monthly_update()` with
`@abstractmethod`. It contains the behavior common to every account while
requiring subclasses to provide their own monthly policy.

```text
BankAccount
├── SavingsAccount   adds monthly interest
└── CurrentAccount   supports an overdraft and monthly fee
```

### Polymorphism

Code can work with a `BankAccount` without knowing which concrete account type
it received. Calling `monthly_update()` selects the correct subclass behavior.

### Encapsulation and properties

Balances, account numbers, and transaction history use private attributes.
Read-only properties expose information without exposing the mutable internal
transaction list.

### Immutable value objects

`Transaction` uses `@dataclass(frozen=True)`. A tuple copy of transaction history
prevents callers from altering the account's records.

### Dependency injection

`Bank` does not construct savings or current accounts. `main.py` constructs them
and injects them through `Bank.add_account()`. The bank therefore coordinates
objects supplied by the caller.

### Money and domain exceptions

Amounts use `Decimal` rather than binary floating-point values. Custom
exceptions distinguish invalid amounts, missing accounts, and insufficient
funds.

### Atomic transfer and rollback

A transfer snapshots both accounts. If either side fails, both balances and
transaction histories are restored.

## Files

- `banking/accounts.py` — account hierarchy and balance rules
- `banking/transaction.py` — immutable transaction records
- `banking/bank.py` — account registration, lookup, and transfers
- `banking/exceptions.py` — banking-specific failures
- `main.py` — composition root and demonstration

## Run

```bash
cd /Users/sebsmith/python/bank
python3 main.py
```

## Design discussion

An abstract base class is appropriate here because account types share real
state and substantial implementation. Protocols are generally more suitable
for replaceable external services that only need to describe supported
operations.

The rollback is suitable for learning but is not database transaction isolation.
A real banking system would persist changes within an ACID database transaction
and would include authorization, auditing, concurrency control, and idempotency.
