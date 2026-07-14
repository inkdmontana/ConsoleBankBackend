from decimal import Decimal

from Models.Account import Account
from Models.Transaction import Transaction
from Repositories.AccountRepository import AccountRepository
from Repositories.UserRepository import UserRepository
from Repositories.TransactionRepository import TransactionRepository


class AccountService:

    def __init__(self):
        self.account_repository = AccountRepository()
        self.user_repository = UserRepository()
        self.transaction_repository = TransactionRepository()

    def create_account(self, user_id, account_type):
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User does not exist.")

        if account_type is None or account_type.strip() == "":
            raise ValueError("Account type is required.")

        account = Account(
            account_id=None,
            user_id=user_id,
            balance=Decimal("0.00"),
            account_type=account_type,
            created_at=None
        )

        created = self.account_repository.create_account(account)

        if not created:
            raise Exception("Account could not be created.")

        return True

    def get_account(self, account_id):
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        return account

    def deposit(self, account_id, amount):
        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        new_balance = account.balance + amount

        updated = self.account_repository.update_balance(
            account_id,
            new_balance
        )

        if not updated:
            raise Exception("Deposit could not be completed.")

        transaction = Transaction(
            txn_id=None,
            account_id=account_id,
            txn_type="Deposit",
            amount=amount,
            created_at=None
        )

        transaction_created = (
            self.transaction_repository.create_transaction(transaction)
        )

        if not transaction_created:
            raise Exception("Transaction record could not be created.")

        return new_balance

    def withdraw(self, account_id, amount):
        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        if amount > account.balance:
            raise ValueError("Insufficient funds.")

        new_balance = account.balance - amount

        updated = self.account_repository.update_balance(
            account_id,
            new_balance
        )

        if not updated:
            raise Exception("Withdrawal could not be completed.")

        transaction = Transaction(
            txn_id=None,
            account_id=account_id,
            txn_type="Withdraw",
            amount=amount,
            created_at=None
        )

        transaction_created = (
            self.transaction_repository.create_transaction(transaction)
        )

        if not transaction_created:
            raise Exception("Transaction record could not be created.")

        return new_balance

    def get_transactions(self, account_id):
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        return self.transaction_repository.find_by_account_id(account_id)