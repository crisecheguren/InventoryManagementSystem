from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, CursorNotFound, DuplicateKeyError, OperationFailure, BulkWriteError
from bson.son import SON
import json

# Constants
PRODUCTS_COLLECTION = "products"


class Database:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def load_sample_data(self):
        """Load sample data into the database if the products collection is empty."""
        try:
            if self.mongo.db[PRODUCTS_COLLECTION].count_documents({}) == 0:
                with open("sample_data.json", "r") as file:
                    data = json.load(file)
                    self.mongo.db[PRODUCTS_COLLECTION].insert_many(data)
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except BulkWriteError as bwe:
            print(f"Error during the bulk insert operation: {bwe.details}")
        except json.JSONDecodeError:
            print("Error decoding the sample data JSON file.")
        except FileNotFoundError:
            print("sample_data.json file not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_product_analytics(self):
        """Return analytics about products grouped by category."""
        pipeline = [
            {
                "$group": {
                    "_id": "$ProductCategory",
                    "count": {"$sum": 1},
                    "average_price": {"$avg": "$Price"},
                    "total_value": {"$sum": {"$multiply": ["$Price", "$AvailableQuantity"]}},
                    "total_quantity": {"$sum": "$AvailableQuantity"},
                    "max_price": {"$max": "$Price"},
                    "min_price": {"$min": "$Price"}
                }
            },
            {
                "$sort": SON([("count", -1), ("_id", -1)])
            }
        ]
        try:
            return list(self.mongo.db[PRODUCTS_COLLECTION].aggregate(pipeline))
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except OperationFailure as e:
            # This exception can occur due to issues with the aggregation operation.
            print(f"Error during the aggregation operation: {e}")
        except Exception as e:
            # Catching other unforeseen exceptions
            print(f"An unexpected error occurred: {e}")
        return []
    
    def create_text_index(self):
        """Create a text index on the ProductName, ProductCategory, and ProductID fields."""
        try:
            self.mongo.db[PRODUCTS_COLLECTION].create_index([("ProductName", "text"), ("ProductCategory", "text"), ("ProductID", "text")])
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except OperationFailure as e:
            print(f"Error during the index creation operation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def search_products(self, query):
        """Search for products using a text index."""
        try:
            return list(self.mongo.db[PRODUCTS_COLLECTION].find({"$text": {"$search": query}}))
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except OperationFailure as e:
            print(f"Error during the search operation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return []
    
    def add_product(self, product):
        """Insert a new product into the products collection."""
        try:
            return self.mongo.db[PRODUCTS_COLLECTION].insert_one(product)
        except DuplicateKeyError:
            print("Duplicate key error. The product already exists.")
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def get_all_products(self):
        try:
            return list(self.mongo.db[PRODUCTS_COLLECTION].find())
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except CursorNotFound:
            print("Cursor not found on the server.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return []

    def get_product_by_id(self, product_id):
        """Fetch a specific product using its ProductID."""
        try:
            return self.mongo.db[PRODUCTS_COLLECTION].find_one({'ProductID': product_id})
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None


    def get_product_by_quantity(self, order="highest"):
        """Retrieve a product based on its quantity."""
        try:
            sort_order = -1 if order == "highest" else 1
            return self.mongo.db[PRODUCTS_COLLECTION].find_one(sort=[("AvailableQuantity", sort_order)])
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except OperationFailure as e:
            print(f"Error during the retrieval operation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def update_product_by_id(self, product_id, data):
        """Update product details using its ProductID."""
        try:
            return self.mongo.db[PRODUCTS_COLLECTION].update_one({'ProductID': product_id}, {"$set": data})
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except OperationFailure as e:
            print(f"Error during the update operation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def delete_product_by_id(self, product_id):
        """Remove a product using its ProductID."""
        try:
            return self.mongo.db[PRODUCTS_COLLECTION].delete_one({'ProductID': product_id})
        except ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        except ServerSelectionTimeoutError:
            print("Server selection timeout error.")
        except OperationFailure as e:
            print(f"Error during the delete operation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None
