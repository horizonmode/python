class BankingError(Exception):
    """Base exception for errors raised by the banking system."""


class InvalidAmountError(BankingError):
    pass


class InsufficientFundsError(BankingError):
    pass


class AccountNotFoundError(BankingError):
    pass
