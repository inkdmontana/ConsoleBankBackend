from db import get_connection
from Models.User import User

class UserRepository:

    def find_by_id(self, user_id):
        connection = get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                SELECT user_id, name, email, created_at
                FROM users
                WHERE user_id = %s
            """

            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result is None:
                return None

            return User(
                result[0],
                result[1],
                result[2],
                result[3]
            )

        except Exception as e:
            print(f"Error finding user: {e}")
            return None

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()

    def create_user(self, user):
        connection = get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
            """

            cursor.execute(query, (
                user.name,
                user.email
            ))

            connection.commit()

            return True

        except Exception as e:
            print(f"Error creating user: {e}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()