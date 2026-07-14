from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import PyMongoError

from mongo_db import get_database
from Models.User import User


class MongoUserRepository:
    

    def __init__(self):
        database = get_database()

        if database is None:
            raise ConnectionError("Could not connect to MongoDB Atlas.")

        self.users_collection = database["users"]

    def find_by_id(self, user_id):
        
        try:
            document = self.users_collection.find_one({"_id": ObjectId(user_id)})

            if document is None:
                return None

            return User(
                user_id=str(document.get("_id")),
                name=document.get("name"),
                email=document.get("email"),
                created_at=document.get("created_at")
            )
                
        except (PyMongoError, InvalidId) as error:
            print(f"Error finding user: {error}")
            return None

    def create_user(self, user):
        
        try:
            document = {
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at or datetime.now()
            }

            result = self.users_collection.insert_one(document)

            return result.inserted_id is not None

        except PyMongoError as error:
            print(f"Error creating user: {error}")
            return False
