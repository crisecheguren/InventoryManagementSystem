
# Inventory Management System

## Introduction

The Inventory Management System offers a flexible and efficient method for managing inventory items. Built around a RESTful API (Flask) and integrated with MongoDB, this system allows for intuitive interactions with inventory data. With Docker support and a dedicated CLI, setup and usage are seamless.

## Features

- **Full-text Search**: Search for products by name, category, or ID.
- **RESTful API**: A comprehensive API for CRUD (Create, Read, Update, Delete) operations on inventory items.
- **Docker Support**: Deploy the system in a Docker environment using the Dockerfile and docker-compose.yml.
- **Command-Line Interface**: A user-friendly cli.py script for easy interactions.
- **MongoDB Integration**: A MongoDB-backed storage system with utilities data handling.
- **Product Analytics**: Aggregate insights on products grouped by category.
- **Sample Data**: Preloaded data from sample_data.json to kickstart your inventory.

## Installation

### Prerequisites

- **Docker**:
    - [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)
    - [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
    - [Docker Engine for Linux](https://docs.docker.com/engine/install/)

### Clone the Repository

```bash
git clone git@github.com:crisecheguren/InventoryManagementSystem.git

cd InventoryManagementSystem
```

### Deploy the Services:

```bash
docker compose up --build
```


## CLI Installation and Usage

To use the CLI, run the following commands from the project directory:

```bash
pip install -r cli-requirements.txt
```


```bash
python cli.py
```

The CLI offers the following commands:

- `add-product`: Adds a new product to the inventory.
- `delete-product`: Deletes a product from the inventory.
- `get-product`: Get a product by its ID.
- `list-products`: Lists all products.
- `search-products`:  Search products based on a query.
- `update-product`: Updates an existing product in the inventory.
- `view-analytics`: Displays aggregated product data.

The system will prompt the user for any relevant information required to execute the command and build the appropriate request.

If the user wishes to skip the prompts, they can pass the required information as command-line arguments. For example, to add a new product, the user can run either of the following commands:

```bash
python cli.py add-product
```

```bash
python cli.py add-product --product-id 123 --product-name "Product Name" --product-category "Category" --price 100 --available-quantity 10
```

Each command can be invoked with a --help flag to view more information about the available options.

```bash
python cli.py add-product --help
```

## Postman Collection

I've also created a Postman collection that can be found here: [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/18806958-ba8e58d1-5514-4bd4-9734-6b27e8d43123?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D18806958-ba8e58d1-5514-4bd4-9734-6b27e8d43123%26entityType%3Dcollection%26workspaceId%3D17b8983f-089d-4ca1-a388-7f888f772367)

### API Endpoint Documentation

## List all products

**Endpoint**: `/products`

**Request Type**: `GET`

**Description**: Returns a list of all products in the inventory.

**Sample Output**:

```JSON
[
    {
        "AvailableQuantity": 324,
        "Price": 999,
        "ProductCategory": "Electronics",
        "ProductID": "1",
        "ProductName": "Toshiba Laptop",
        "_id": "64d25a2a43649728777c5807"
    },
    {
        "AvailableQuantity": 351,
        "Price": 762,
        "ProductCategory": "Electronics",
        "ProductID": "2",
        "ProductName": "Smartphone",
        "_id": "64d25a2a43649728777c5808"
    },
    {
        "AvailableQuantity": 89,
        "Price": 83,
        "ProductCategory": "Electronics",
        "ProductID": "3",
        "ProductName": "Headphones",
        "_id": "64d25a2a43649728777c5809"
    }
]
```

## Fetch a specific product

**Endpoint**: `/products/{product_id}`

**Request Type**: `GET`

**Description**: Returns a specific product using the ProductID provided.

**Sample Request**: `/products/1`

**Sample Output**:

```JSON
{
    "AvailableQuantity": 499,
    "Price": 1572,
    "ProductCategory": "Electronics",
    "ProductID": "1",
    "ProductName": "Laptop",
    "_id": "64d3ec2a5e3e680957dd0147"
}
```

## Get analytics for products

**Endpoint**: `/products/analytics`

**Request Type**: `GET`

**Description**: Returns aggregated data for products grouped by category and information about the least and most stocked product.

**Sample Output**:

```JSON
[    
    {
        "average_price": 545.2,
        "category": "Appliances",
        "count": 5,
        "max_price": 1213,
        "min_price": 54,
        "total_quantity": 1125,
        "total_value": 351877
    },
    {
        "average_price": 51.0,
        "category": "Apparel",
        "count": 5,
        "max_price": 135,
        "min_price": 11,
        "total_quantity": 1511,
        "total_value": 88299
    },
    {
        "least_stocked_product": {
            "AvailableQuantity": 20,
            "Price": 877,
            "ProductCategory": "Electronics",
            "ProductID": "4",
            "ProductName": "TV",
            "_id": "64d3ec2a5e3e680957dd014a"
        },
        "most_stocked_product": {
            "AvailableQuantity": 499,
            "Price": 1572,
            "ProductCategory": "Electronics",
            "ProductID": "1",
            "ProductName": "Laptop",
            "_id": "64d3ec2a5e3e680957dd0147"
        }
    }
]
```

## Search for products

**Endpoint**: `/products/search`

**Request Type**: `GET`

**Description**: Returns a list of products that match the search query.

**Sample Query**:
```
http://localhost:5000/products/search?q=electronics
```
**Sample Output**:

```JSON
[
    {
        "AvailableQuantity": 324,
        "Price": 999,
        "ProductCategory": "Electronics",
        "ProductID": "1",
        "ProductName": "Toshiba Laptop",
        "_id": "64d25a2a43649728777c5807"
    },
    {
        "AvailableQuantity": 351,
        "Price": 762,
        "ProductCategory": "Electronics",
        "ProductID": "2",
        "ProductName": "Smartphone",
        "_id": "64d25a2a43649728777c5808"
    },
     {
        "AvailableQuantity": 20,
        "Price": 877,
        "ProductCategory": "Electronics",
        "ProductID": "4",
        "ProductName": "TV",
        "_id": "64d3ec2a5e3e680957dd014a"
    }
]
```

## Add a new product

**Endpoint**: `/products`

**Request Type**: `POST`

**Description**: Adds a new product to the inventory.

**Sample Request**:

```JSON
{
    "ProductID": "31",
    "ProductName": "Electric Piano",
    "ProductCategory": "Electronics",
    "Price": 3200,
    "AvailableQuantity": 20
}
```

**Sample Output**:

```JSON
{
    "ProductID": "31",
    "message": "Product added successfully"
}
```

## Update a product

**Endpoint**: `/products/{product_id}`

**Request Type**: `PUT`

**Description**: Updates a product in the inventory.

**Sample Request**:

```JSON
{
    "ProductID": "31",
    "ProductName": "Synthesizer",
    "ProductCategory": "Electronics",
    "Price": 1600,
    "AvailableQuantity": 5
}
```

**Sample Output**:

```JSON
{
    "message": "Product updated successfully"
}
```

## Delete a product

**Endpoint**: `/products/{product_id}`

**Request Type**: `DELETE`

**Description**: Deletes a product from the inventory.

**Sample Output**:

```JSON
{
    "message": "Product deleted successfully"
}
```