from flask import Flask, request, jsonify, abort
from http import HTTPStatus
from db import Database
from typing import Dict, Any

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://db:27017/flaskdb"
db = Database(app)

db.load_sample_data()
db.create_text_index()


def object_id_to_string(product: Dict[str, Any]) -> None:
    """
    MongoDB uses ObjectId for the "_id" field by default.
    Since ObjectId is not JSON serializable, we convert it to a string.
    """
    if product and '_id' in product:
        product['_id'] = str(product['_id'])

def validate_product_data(data):
    """Validate and sanitize product data."""
    
    """Ensure that ProductID is a string"""
    if 'ProductID' in data:
        data['ProductID'] = str(data['ProductID'])

    """Validate AvailableQuantity and Price"""
    fields_to_validate = ['AvailableQuantity', 'Price']
    for field in fields_to_validate:
        if field in data:
            try:
                data[field] = int(data[field])
            except ValueError:
                return False, jsonify({"message": f"Invalid {field} value"}), HTTPStatus.BAD_REQUEST

    return True, None, None


@app.route('/products', methods=['POST'])
def add_product():
    """Extract the JSON data from the request."""
    data = request.get_json()


    """Validate product data"""
    is_valid, error_response, status_code = validate_product_data(data)
    if not is_valid:
        return error_response, status_code

    """Check if a product with this ProductID already exists and return 409 if it does."""
    existing_product = db.get_product_by_id(data['ProductID'])
    if existing_product:
        return jsonify({"message": "ProductID already exists"}), HTTPStatus.CONFLICT

    """Insert the data as a new document in the MongoDB products collection."""
    result = db.add_product(data)

    """If the insert was successful, the insert_one method returns an InsertOneResult object.
    We can get the ID of the new document from this object."""
    if result.acknowledged:
        """Return a successful response with the ID of the new product."""
        return jsonify({"ProductID": data['ProductID'], "message": "Product added successfully"}), HTTPStatus.CREATED
    
    """If the insert was not successful, return a 500 error."""
    return jsonify({"message": "Failed to add product"}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/products/<id>', methods=['PUT'])
def update_product_by_id(id: str):
    """Extract the JSON data from the request."""
    data = request.get_json()
    
    """Validate product data"""
    is_valid, error_response, status_code = validate_product_data(data)
    if not is_valid:
        return error_response, status_code

    """Check if a product with this ProductID (from the payload) already exists and if it belongs to another product."""
    product_id_from_payload = data.get('ProductID', None)
    if product_id_from_payload:
        existing_product = db.get_product_by_id(product_id_from_payload)
        if existing_product and existing_product['ProductID'] != id:
            return jsonify({"message": "ProductID already exists"}), HTTPStatus.CONFLICT



    """Update the document in the MongoDB products collection with the given ID."""
    result = db.update_product_by_id(id, data)
    
    """If no document was found with the given ID, return a 404 error."""
    if result.matched_count == 0:
        return jsonify({"message": "ID does not exist"}), HTTPStatus.NOT_FOUND
    
    """If the update was successful, return 200."""
    return jsonify({"message": "Product updated successfully"}), HTTPStatus.OK


@app.route('/products/analytics', methods=['GET'])
def get_product_analytics():
    """Returns analytics about the products in the database."""
    results = db.get_product_analytics()
    
    """The '$group' stage of MongoDB's aggregation framework uses '_id' as a special field to define the grouping criteria.
    Here we convert the '_id' field to 'category' for a more user-friendly response and cleaner looking code in cli.py."""
    for result in results:
        result['category'] = result.pop('_id')

    """Get the most and least stocked products."""
    most_stocked_product = db.get_product_by_quantity("highest")
    print("Most stocked:", most_stocked_product)
    least_stocked_product = db.get_product_by_quantity("lowest")
    print("Least stocked:", least_stocked_product)
    
    object_id_to_string(most_stocked_product)
    object_id_to_string(least_stocked_product)

    """Add the most and least stocked products to the response."""
    results.append({"most_stocked_product": most_stocked_product, "least_stocked_product": least_stocked_product})

    return jsonify(results), HTTPStatus.OK


@app.route('/products', methods=['GET'])
def get_all_products():
    """Returns a list of all products in the database."""
    products = db.get_all_products()
    
    for product in products:
        object_id_to_string(product)

    return jsonify(products)


@app.route('/products/<id>', methods=['GET'])
def get_product_by_id(id: str):
    """Returns a single product from the database."""
    product = db.get_product_by_id(id)
    
    if product is None:
        abort(HTTPStatus.NOT_FOUND)

    object_id_to_string(product)
    return jsonify(product)

@app.route('/products/search', methods=['GET'])
def search_products():
    """Search for products based on the given query."""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"message": "Query parameter 'q' is required"}), HTTPStatus.BAD_REQUEST
    search_results = db.search_products(query)
    for product in search_results:
        object_id_to_string(product)
    return jsonify(search_results)


@app.route('/products/<id>', methods=['DELETE'])
def delete_product_by_id(id: str):
    """Deletes a single product from the database."""
    
    result = db.delete_product_by_id(id)
    
    if result.deleted_count == 0:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify({"message": "Product deleted successfully"}), HTTPStatus.OK


@app.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error=None):
    """Handle 404 errors by returning a JSON response and the requested URL."""
    message = {
        'status': HTTPStatus.NOT_FOUND,
        'message': f'Not Found: {request.url}',
    }
    resp = jsonify(message)
    resp.status_code = HTTPStatus.NOT_FOUND
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
