from .accounts import BankAccount, to_money
from .exceptions import (
    AccountNotFoundError,
    BankingError,
    InsufficientFundsError,
    InvalidAmountError,
)


class Bank:
    bank_count = 0

    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Bank name cannot be empty.")
        self.name = name.strip()
        self.__accounts: dict[str, BankAccount] = {}
        type(self).bank_count += 1

    @staticmethod
    def validate_account(account: object) -> bool:
        return isinstance(account, BankAccount)

    @classmethod
    def get_bank_count(cls) -> int:
        return cls.bank_count

    def add_account(self, account: BankAccount) -> None:
        if not self.validate_account(account):
            raise TypeError("account must be a BankAccount")
        if account.account_number in self.__accounts:
            raise ValueError(
                f"Account '{account.account_number}' has already been added."
            )
        self.__accounts[account.account_number] = account

    def find_account(self, account_number: str) -> BankAccount:
        try:
            return self.__accounts[account_number]
        except KeyError as error:
            raise AccountNotFoundError(
                f"Account '{account_number}' was not found."
            ) from error

    def transfer(self, sender_number: str, recipient_number: str, amount) -> None:
        amount = to_money(amount)
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be greater than zero.")
        if sender_number == recipient_number:
            raise BankingError("Cannot transfer money to the same account.")

        sender = self.find_account(sender_number)
        recipient = self.find_account(recipient_number)

        if not sender.can_withdraw(amount):
            raise InsufficientFundsError(
                f"Account {sender_number} has insufficient funds."
            )

        sender_snapshot = sender._create_snapshot()
        recipient_snapshot = recipient._create_snapshot()

        try:
            sender._debit(
                amount,
                "transfer out",
                f"Transfer to {recipient_number}",
            )
            recipient._credit(
                amount,
                "transfer in",
                f"Transfer from {sender_number}",
            )
        except Exception:
            sender._restore_snapshot(sender_snapshot)
            recipient._restore_snapshot(recipient_snapshot)
            raise

    def list_accounts(self) -> None:
        if not self.__accounts:
            print("This bank has no accounts.")
            return
        for account in self.__accounts.values():
            print(account)
