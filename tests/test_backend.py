from Services.MySQLAccountService import AccountService


service = AccountService()


def test_get_account():
    print("\n----- GET ACCOUNT -----")

    try:
        account = service.get_account(6)

        print("Account Retrieved Successfully")
        print(f"Account ID: {account.account_id}")
        print(f"User ID: {account.user_id}")
        print(f"Balance: ${account.balance}")
        print(f"Account Type: {account.account_type}")

    except Exception as e:
        print(e)


def test_deposit():
    print("\n----- DEPOSIT -----")

    try:
        new_balance = service.deposit(6, 250)

        print("Deposit Successful")
        print(f"New Balance: ${new_balance}")

    except Exception as e:
        print(e)


def test_withdraw():
    print("\n----- WITHDRAW -----")

    try:
        new_balance = service.withdraw(6, 100)

        print("Withdrawal Successful")
        print(f"New Balance: ${new_balance}")

    except Exception as e:
        print(e)


def test_transactions():
    print("\n----- TRANSACTION HISTORY -----")

    try:
        transactions = service.get_transactions(6)

        for transaction in transactions:
            print(
                f"ID: {transaction.txn_id} | "
                f"Type: {transaction.txn_type} | "
                f"Amount: ${transaction.amount} | "
                f"Date: {transaction.created_at}"
            )

    except Exception as e:
        print(e)


if __name__ == "__main__":

    test_get_account()

    test_deposit()

    test_withdraw()

    test_transactions()