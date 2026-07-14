import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE")


def get_database():
    try:
        client = MongoClient(MONGODB_URI)

        client.admin.command("ping")

        print("Connected to MongoDB Atlas successfully!")

        return client[DATABASE_NAME]

    except PyMongoError as e:
        print(f"MongoDB connection failed: {e}")
        return None