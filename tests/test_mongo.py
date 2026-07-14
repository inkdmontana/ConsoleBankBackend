from mongo_db import get_database

database = get_database()

if database is not None:
    print(f"Database: {database.name}")

    print("\nCollections:")

    for collection in database.list_collection_names():
        print("-", collection)