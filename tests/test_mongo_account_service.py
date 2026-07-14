from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from Models.Account import Account
from Services.MongoAccountService import MongoAccountService


@pytest.fixture
def service():
    service = MongoAccountService()

    service.account_repository = MagicMock()
    service.user_repository = MagicMock()
    service.transaction_repository = MagicMock()

    return service


def test_get_account_returns_account(service):
    expected_account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = expected_account

    result = service.get_account("account123")

    assert result == expected_account
    service.account_repository.find_by_id.assert_called_once_with("account123")


def test_get_account_raises_error_when_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.get_account("missing-account")


def test_deposit_rejects_zero(service):
    with pytest.raises(
        ValueError,
        match="Deposit amount must be positive."
    ):
        service.deposit("account123", 0)


def test_deposit_rejects_negative_amount(service):
    with pytest.raises(
        ValueError,
        match="Deposit amount must be positive."
    ):
        service.deposit("account123", -50)

def test_deposit_success(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = True

    result = service.deposit("account123", 250)

    assert result == Decimal("1250.00")

    service.account_repository.update_balance.assert_called_once_with(
        "account123",
        Decimal("1250.00")
    )

    service.transaction_repository.create_transaction.assert_called_once()


def test_deposit_raises_error_when_account_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.deposit("missing-account", 100)


def test_deposit_raises_error_when_balance_update_fails(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = False

    with pytest.raises(Exception, match="Deposit could not be completed."):
        service.deposit("account123", 100)


def test_deposit_raises_error_when_transaction_creation_fails(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = False

    with pytest.raises(
        Exception,
        match="Transaction record could not be created."
    ):
        service.deposit("account123", 100)

def test_withdraw_success(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = True

    result = service.withdraw("account123", 250)

    assert result == Decimal("750.00")

    service.account_repository.update_balance.assert_called_once_with(
        "account123",
        Decimal("750.00")
    )

    service.transaction_repository.create_transaction.assert_called_once()


def test_withdraw_rejects_zero(service):
    with pytest.raises(
        ValueError,
        match="Withdrawal amount must be positive."
    ):
        service.withdraw("account123", 0)


def test_withdraw_rejects_negative_amount(service):
    with pytest.raises(
        ValueError,
        match="Withdrawal amount must be positive."
    ):
        service.withdraw("account123", -50)


def test_withdraw_raises_error_when_account_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Account not found."):
        service.withdraw("missing-account", 100)


def test_withdraw_rejects_overdraft(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("100.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account

    with pytest.raises(ValueError, match="Insufficient funds."):
        service.withdraw("account123", 200)


def test_withdraw_raises_error_when_balance_update_fails(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = False

    with pytest.raises(Exception, match="Withdrawal could not be completed."):
        service.withdraw("account123", 100)


def test_withdraw_raises_error_when_transaction_creation_fails(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    service.account_repository.find_by_id.return_value = account
    service.account_repository.update_balance.return_value = True
    service.transaction_repository.create_transaction.return_value = False

    with pytest.raises(
        Exception,
        match="Transaction record could not be created."
    ):
        service.withdraw("account123", 100)

def test_create_account_success(service):
    service.user_repository.find_by_id.return_value = MagicMock()
    service.account_repository.create_account.return_value = True

    result = service.create_account(
        "user123",
        "Checking"
    )

    assert result is True

    service.user_repository.find_by_id.assert_called_once_with("user123")
    service.account_repository.create_account.assert_called_once()


def test_create_account_user_not_found(service):
    service.user_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User does not exist."):
        service.create_account("user123", "Checking")


def test_create_account_blank_account_type(service):
    service.user_repository.find_by_id.return_value = MagicMock()

    with pytest.raises(ValueError, match="Account type is required."):
        service.create_account("user123", "")


def test_create_account_repository_failure(service):
    service.user_repository.find_by_id.return_value = MagicMock()
    service.account_repository.create_account.return_value = False

    with pytest.raises(
        Exception,
        match="Account could not be created."
    ):
        service.create_account(
            "user123",
            "Checking"
        )

def test_get_transactions_success(service):
    account = Account(
        account_id="account123",
        user_id="user123",
        balance=Decimal("1000.00"),
        account_type="Checking"
    )

    expected_transactions = [
        MagicMock(),
        MagicMock()
    ]

    service.account_repository.find_by_id.return_value = account
    service.transaction_repository.find_by_account_id.return_value = (
        expected_transactions
    )

    result = service.get_transactions("account123")

    assert result == expected_transactions

    service.transaction_repository.find_by_account_id.assert_called_once_with(
        "account123"
    )


def test_get_transactions_account_not_found(service):
    service.account_repository.find_by_id.return_value = None

    with pytest.raises(
        ValueError,
        match="Account not found."
    ):
        service.get_transactions("account123")