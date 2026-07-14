from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from Models.Account import Account
from Services.MySQLAccountService import AccountService


@pytest.fixture
def service():
    service = AccountService()

    service.account_repository = MagicMock()
    service.user_repository = MagicMock()
    service.transaction_repository = MagicMock()

    return service


def test_get_account_returns_account(service):
    expected_account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = expected_account

    result = service.get_account(1)

    assert result == expected_account
    service.account_repository.find_by_id.assert_called_once_with(1)


def test_get_account_raises_error_when_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.get_account(999)


def test_create_account_success(service):
    service.user_repository.find_by_id.return_value = MagicMock()
    service.account_repository.create_account.return_value = True

    result = service.create_account(1, "Checking")

    assert result is True

    service.user_repository.find_by_id.assert_called_once_with(1)
    service.account_repository.create_account.assert_called_once()


def test_create_account_user_not_found(service):
    service.user_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User does not exist."):
        service.create_account(999, "Checking")


def test_create_account_blank_account_type(service):
    service.user_repository.find_by_id.return_value = MagicMock()

    with pytest.raises(ValueError, match="Account type is required."):
        service.create_account(1, "")


def test_create_account_repository_failure(service):
    service.user_repository.find_by_id.return_value = MagicMock()
    service.account_repository.create_account.return_value = False

    with pytest.raises(
        Exception,
        match="Account could not be created."
    ):
        service.create_account(1, "Checking")

def test_deposit_success(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = True

    result = service.deposit(1, 250)

    assert result == Decimal("1250.00")

    service.account_repository.update_balance.assert_called_once_with(
        1,
        Decimal("1250.00")
    )

    service.transaction_repository.create_transaction.assert_called_once()


def test_deposit_rejects_zero(service):
    with pytest.raises(
        ValueError,
        match="Deposit amount must be positive."
    ):
        service.deposit(1, 0)


def test_deposit_rejects_negative_amount(service):
    with pytest.raises(
        ValueError,
        match="Deposit amount must be positive."
    ):
        service.deposit(1, -50)


def test_deposit_account_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.deposit(999, 100)


def test_deposit_balance_update_failure(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = False

    with pytest.raises(Exception, match="Deposit could not be completed."):
        service.deposit(1, 100)


def test_deposit_transaction_creation_failure(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = False

    with pytest.raises(
        Exception,
        match="Transaction record could not be created."
    ):
        service.deposit(1, 100)

def test_withdraw_success(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = True

    result = service.withdraw(1, 250)

    assert result == Decimal("750.00")

    service.account_repository.update_balance.assert_called_once_with(
        1,
        Decimal("750.00")
    )

    service.transaction_repository.create_transaction.assert_called_once()


def test_withdraw_rejects_zero(service):
    with pytest.raises(
        ValueError,
        match="Withdrawal amount must be positive."
    ):
        service.withdraw(1, 0)


def test_withdraw_rejects_negative_amount(service):
    with pytest.raises(
        ValueError,
        match="Withdrawal amount must be positive."
    ):
        service.withdraw(1, -50)


def test_withdraw_account_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.withdraw(999, 100)


def test_withdraw_rejects_overdraft(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("100.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account

    with pytest.raises(ValueError, match="Insufficient funds."):
        service.withdraw(1, 200)


def test_withdraw_balance_update_failure(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = False

    with pytest.raises(
        Exception,
        match="Withdrawal could not be completed."
    ):
        service.withdraw(1, 100)


def test_withdraw_transaction_creation_failure(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = False

    with pytest.raises(
        Exception,
        match="Transaction record could not be created."
    ):
        service.withdraw(1, 100)

def test_get_transactions_success(service):
    account = Account(
        account_id=1,
        user_id=1,
        balance=Decimal("1000.00"),
        account_type="Checking",
        created_at=None
    )

    expected_transactions = [
        MagicMock(),
        MagicMock()
    ]

    service.account_repository.find_by_id.return_value = account
    service.transaction_repository.find_by_account_id.return_value = (
        expected_transactions
    )

    result = service.get_transactions(1)

    assert result == expected_transactions

    service.transaction_repository.find_by_account_id.assert_called_once_with(
        1
    )


def test_get_transactions_account_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.get_transactions(999)