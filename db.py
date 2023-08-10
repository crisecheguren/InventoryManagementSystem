from flask_pymongo import PyMongo
from bson.son import SON
import json

# Constants
PRODUCTS_COLLECTION = "products"


class Database:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def load_sample_data(self):
        """Load sample data into the database if the products collection is empty."""
        if self.mongo.db[PRODUCTS_COLLECTION].count_documents({}) == 0:
            with open("sample_data.json", "r") as file:
                data = json.load(file)
                self.mongo.db[PRODUCTS_COLLECTION].insert_many(data)

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
        return list(self.mongo.db[PRODUCTS_COLLECTION].aggregate(pipeline))
    
    def create_text_index(self):
        """Create a text index on the ProductName, ProductCategory and ProductID fields."""
        self.mongo.db[PRODUCTS_COLLECTION].create_index([("ProductName", "text"), ("ProductCategory", "text"), ("ProductID", "text")])

    def search_products(self, query):
        """Search for products using a text index."""
        return list(self.mongo.db[PRODUCTS_COLLECTION].find({"$text": {"$search": query}}))
    
    def add_product(self, product):
        """Insert a new product into the products collection."""
        return self.mongo.db[PRODUCTS_COLLECTION].insert_one(product)

    def get_all_products(self):
        """Retrieve all products from the products collection."""
        return list(self.mongo.db[PRODUCTS_COLLECTION].find())

    def get_product_by_id(self, product_id):
        """Fetch a specific product using its ProductID."""
        return self.mongo.db[PRODUCTS_COLLECTION].find_one({'ProductID': product_id})

    def get_product_by_quantity(self, order="highest"):
        """Retrieve a product based on its quantity."""

        sort_order = -1 if order == "highest" else 1
        return self.mongo.db[PRODUCTS_COLLECTION].find_one(sort=[("AvailableQuantity", sort_order)])

    def update_product_by_id(self, product_id, data):
        """Update product details using its ProductID."""
        return self.mongo.db[PRODUCTS_COLLECTION].update_one({'ProductID': product_id}, {"$set": data})

    def delete_product_by_id(self, product_id):
        """Remove a product using its ProductID."""
        return self.mongo.db[PRODUCTS_COLLECTION].delete_one({'ProductID': product_id})
