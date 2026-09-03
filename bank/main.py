from decimal import Decimal

from banking import Bank, BankingError, CurrentAccount, SavingsAccount


def main() -> None:
    bank = Bank("Python Bank")

    alice = SavingsAccount(
        owner="Alice",
        opening_balance=Decimal("1000.00"),
        interest_rate=Decimal("0.03"),
    )
    bob = CurrentAccount(
        owner="Bob",
        opening_balance=Decimal("200.00"),
        overdraft_limit=Decimal("500.00"),
    )

    # Inject the account objects into Bank. Bank does not construct them.
    bank.add_account(alice)
    bank.add_account(bob)

    try:
        bank.transfer(
            alice.account_number,
            bob.account_number,
            Decimal("125.50"),
        )
        bob.withdraw(Decimal("400.00"))
        alice.monthly_update()
        bob.monthly_update()
    except BankingError as error:
        print(f"Banking error: {error}")

    print("\nAccounts:")
    bank.list_accounts()
    alice.display_transactions()
    bob.display_transactions()
    print(f"\nBanks created: {Bank.get_bank_count()}")


if __name__ == "__main__":
    main()
