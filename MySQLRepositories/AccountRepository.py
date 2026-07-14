from mysql_db import get_connection
from Models.Account import Account


class AccountRepository:

    def find_by_id(self, account_id):
        connection = get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                SELECT account_id, user_id, balance, account_type, created_at
                FROM accounts
                WHERE account_id = %s
            """

            cursor.execute(query, (account_id,))
            result = cursor.fetchone()

            if result is None:
                return None

            return Account(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4]
            )

        except Exception as e:
            print(f"Error finding account: {e}")
            return None

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()

    def create_account(self, account):
        connection = get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO accounts (user_id, balance, account_type)
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (
                account.user_id,
                account.balance,
                account.account_type
            ))

            connection.commit()
            return True

        except Exception as e:
            print(f"Error creating account: {e}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()

    def update_balance(self, account_id, new_balance):
        connection = get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                UPDATE accounts
                SET balance = %s
                WHERE account_id = %s
            """

            cursor.execute(query, (
                new_balance,
                account_id
            ))

            connection.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error updating account balance: {e}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()