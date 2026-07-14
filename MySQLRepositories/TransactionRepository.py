from mysql_db import get_connection
from Models.Transaction import Transaction


class TransactionRepository:

    def create_transaction(self, transaction):
        connection = get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO transactions (account_id, txn_type, amount)
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (
                transaction.account_id,
                transaction.txn_type,
                transaction.amount
            ))

            connection.commit()
            return True

        except Exception as e:
            print(f"Error creating transaction: {e}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()

    def find_by_account_id(self, account_id):
        connection = get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                SELECT txn_id, account_id, txn_type, amount, created_at
                FROM transactions
                WHERE account_id = %s
                ORDER BY created_at DESC
            """

            cursor.execute(query, (account_id,))
            results = cursor.fetchall()

            transactions = []

            for result in results:
                transaction = Transaction(
                    result[0],
                    result[1],
                    result[2],
                    result[3],
                    result[4]
                )

                transactions.append(transaction)

            return transactions

        except Exception as e:
            print(f"Error finding transactions: {e}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()