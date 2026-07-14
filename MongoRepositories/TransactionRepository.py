from datetime import datetime
from decimal import Decimal

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import PyMongoError

from mongo_db import get_database
from Models.Transaction import Transaction


class MongoTransactionRepository:
   
    def __init__(self):
        database = get_database()

        if database is None:
            raise ConnectionError("Could not connect to MongoDB Atlas.")

        self.transactions_collection = database["transactions"]

    def find_by_account_id(self, account_id):
       
        try:
            documents = self.transactions_collection.find({
                "account_id": ObjectId(account_id)
            }).sort("created_at", -1)
            
            transactions = []
            for document in documents:
                transaction = Transaction(
                    txn_id=str(document["_id"]),
                    account_id=str(document["account_id"]),
                    txn_type=document["txn_type"],
                    amount=Decimal(str(document["amount"])),
                    created_at=document.get("created_at")
                )
                transactions.append(transaction)

            return transactions

        except InvalidId:
            print("Invalid account ID.")
            return []

        except PyMongoError as error:
            print(f"Error retrieving transactions: {error}")
            return []

    def create_transaction(self, transaction):
        
        try:
            document = {
                "account_id": ObjectId(transaction.account_id),
                "txn_type": transaction.txn_type,
                "amount": float(transaction.amount),
                "created_at": transaction.created_at or datetime.now()
            }

            result = self.transactions_collection.insert_one(document)

            return result.inserted_id is not None

        except InvalidId:
            print("Invalid account ID.")
            return False

        except PyMongoError as error:
            print(f"Error creating transaction: {error}")
            return False
