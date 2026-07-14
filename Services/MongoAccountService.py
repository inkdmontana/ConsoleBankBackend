from decimal import Decimal

from Models.Account import Account
from Models.Transaction import Transaction
from MongoRepositories.AccountRepository import MongoAccountRepository
from MongoRepositories.UserRepository import MongoUserRepository
from MongoRepositories.TransactionRepository import MongoTransactionRepository


class MongoAccountService:
    """Service layer for account operations using MongoDB repositories."""

    def __init__(
        self,
        account_repository=None,
        user_repository=None,
        transaction_repository=None
    ):
        self.account_repository = (
            account_repository or MongoAccountRepository()
        )
        self.user_repository = (
            user_repository or MongoUserRepository()
        )
        self.transaction_repository = (
            transaction_repository or MongoTransactionRepository()
        )

    def create_account(self, user_id, account_type):
        """Create a new account for a user."""
        # Validate that the user exists
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User does not exist.")

        # Validate account type is provided
        if account_type is None or account_type.strip() == "":
            raise ValueError("Account type is required.")

        # Create account with initial balance of 0.00
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
        """Retrieve an account by account ID."""
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        return account

    def deposit(self, account_id, amount):
        """Deposit money into an account and create a transaction record."""
        # Convert amount to Decimal for precision
        amount = Decimal(str(amount))

        # Validate deposit amount is positive
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        # Retrieve the account
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        # Calculate new balance
        new_balance = account.balance + amount

        # Update account balance
        updated = self.account_repository.update_balance(
            account_id,
            new_balance
        )

        if not updated:
            raise Exception("Deposit could not be completed.")

        # Create transaction record
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
        """Withdraw money from an account and create a transaction record."""
        # Convert amount to Decimal for precision
        amount = Decimal(str(amount))

        # Validate withdrawal amount is positive
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        # Retrieve the account
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        # Validate sufficient funds
        if amount > account.balance:
            raise ValueError("Insufficient funds.")

        # Calculate new balance
        new_balance = account.balance - amount

        # Update account balance
        updated = self.account_repository.update_balance(
            account_id,
            new_balance
        )

        if not updated:
            raise Exception("Withdrawal could not be completed.")

        # Create transaction record
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
        """Get all transactions for a specific account."""
        # Validate that the account exists
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        return self.transaction_repository.find_by_account_id(account_id)

