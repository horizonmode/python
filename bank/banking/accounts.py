from abc import ABC, abstractmethod
from decimal import Decimal
from itertools import count

from .exceptions import InvalidAmountError, InsufficientFundsError
from .transaction import Transaction


def to_money(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


class BankAccount(ABC):
    _account_number_sequence = count(1)

    def __init__(self, owner: str, opening_balance=Decimal("0.00")):
        opening_balance = to_money(opening_balance)

        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("The owner's name cannot be empty.")
        if opening_balance < 0:
            raise InvalidAmountError("Opening balance cannot be negative.")

        self.__account_number = (
            f"ACC{next(self._account_number_sequence):06d}"
        )
        self.__owner = owner.strip()
        self.__balance = Decimal("0.00")
        self.__transactions: list[Transaction] = []

        if opening_balance > 0:
            self._credit(opening_balance, "deposit", "Opening balance")

    @property
    def account_number(self) -> str:
        return self.__account_number

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def balance(self) -> Decimal:
        return self.__balance

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        return tuple(self.__transactions)

    @staticmethod
    def _validate_amount(amount) -> Decimal:
        amount = to_money(amount)
        if amount <= 0:
            raise InvalidAmountError(
                "Transaction amount must be greater than zero."
            )
        return amount

    def _credit(self, amount, transaction_type: str, description: str) -> None:
        amount = self._validate_amount(amount)
        self.__balance += amount
        self.__transactions.append(
            Transaction(transaction_type, amount, description)
        )

    def _debit(self, amount, transaction_type: str, description: str) -> None:
        amount = self._validate_amount(amount)
        if not self.can_withdraw(amount):
            raise InsufficientFundsError(
                f"Account {self.account_number} has insufficient funds."
            )
        self.__balance -= amount
        self.__transactions.append(
            Transaction(transaction_type, amount, description)
        )

    def deposit(self, amount, description="Cash deposit") -> None:
        self._credit(amount, "deposit", description)

    def withdraw(self, amount, description="Cash withdrawal") -> None:
        self._debit(amount, "withdrawal", description)

    def can_withdraw(self, amount) -> bool:
        amount = self._validate_amount(amount)
        return amount <= self.balance

    def _create_snapshot(self) -> tuple[Decimal, int]:
        return self.__balance, len(self.__transactions)

    def _restore_snapshot(self, snapshot: tuple[Decimal, int]) -> None:
        previous_balance, transaction_count = snapshot
        self.__balance = previous_balance
        del self.__transactions[transaction_count:]

    def display_transactions(self) -> None:
        print(f"\nTransactions for {self.account_number}:")
        if not self.__transactions:
            print("No transactions.")
            return
        for transaction in self.__transactions:
            print(transaction)

    @abstractmethod
    def monthly_update(self) -> None:
        pass

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}(account_number={self.account_number}, "
            f"owner={self.owner}, balance=£{self.balance:.2f})"
        )


class SavingsAccount(BankAccount):
    def __init__(
        self,
        owner: str,
        opening_balance=Decimal("0.00"),
        interest_rate=Decimal("0.03"),
    ):
        self.interest_rate = Decimal(str(interest_rate))
        if self.interest_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        super().__init__(owner, opening_balance)

    def monthly_update(self) -> None:
        monthly_interest = to_money(
            self.balance * self.interest_rate / Decimal("12")
        )
        if monthly_interest > 0:
            self._credit(
                monthly_interest,
                "interest",
                "Monthly savings interest",
            )


class CurrentAccount(BankAccount):
    def __init__(
        self,
        owner: str,
        opening_balance=Decimal("0.00"),
        overdraft_limit=Decimal("0.00"),
        monthly_overdraft_fee=Decimal("10.00"),
    ):
        self.overdraft_limit = to_money(overdraft_limit)
        self.monthly_overdraft_fee = to_money(monthly_overdraft_fee)

        if self.overdraft_limit < 0:
            raise ValueError("Overdraft limit cannot be negative.")
        if self.monthly_overdraft_fee < 0:
            raise ValueError("Monthly fee cannot be negative.")

        super().__init__(owner, opening_balance)

    def can_withdraw(self, amount) -> bool:
        amount = self._validate_amount(amount)
        return self.balance - amount >= -self.overdraft_limit

    def monthly_update(self) -> None:
        if self.balance < 0 and self.monthly_overdraft_fee > 0:
            self._debit(
                self.monthly_overdraft_fee,
                "fee",
                "Monthly overdraft fee",
            )
