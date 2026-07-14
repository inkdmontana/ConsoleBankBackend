class User:

    def __init__(self, user_id, name, email, created_at=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Email: {self.email}"