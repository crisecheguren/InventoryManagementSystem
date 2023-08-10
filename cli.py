# Import the necessary modules for the CLI and for making HTTP requests.
import click
import requests

# Define the base URL for our API endpoints.
BASE_URL = "http://localhost:5000/products"

# Create a new group for our CLI commands.
@click.group()
def cli():
    """Inventory Management CLI."""
    pass

# Helper function to print product details
def print_product_details(product):
     return f"ID: {product['ProductID']}, Name: {product['ProductName']}, Category: {product['ProductCategory']}, Price: {product['Price']}, Available Quantity: {product['AvailableQuantity']}"

# Define a command to view product analytics.
@cli.command(help="Displays aggregated product data.")
def view_analytics():
    response = requests.get(f"{BASE_URL}/analytics")
    
    if response.status_code == 200:
        response_json = response.json()

        click.echo("\nProduct Analytics:\n")

        # Loop through each aggregated item and print its details.
        for item in response_json[:-1]:
            click.echo(f"\nCategory: {item['category']}")
            click.echo(f"Product Count: {item['count']}")
            click.echo(f"Total Quantity: {item['total_quantity']}")
            click.echo(f"Average Price: {item['average_price']:.2f}")
            click.echo(f"Max Price: {item['max_price']}")
            click.echo(f"Min Price: {item['min_price']}")
            click.echo(f"Total Value: {item['total_value']:.2f}")
        
        # Print the most and least stocked product details.
        click.echo(f"\nMost Stocked Product: \n{print_product_details(response_json[-1]['most_stocked_product'])}")
        

        click.echo(f"\nLeast Stocked Product: \n{print_product_details(response_json[-1]['least_stocked_product'])}\n")
        
    else:
        click.echo("\nFailed to retrieve product analytics.\n")

# Define a command to list all products.
@cli.command(help="Lists all products.")
def list_products():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        products = response.json()
        click.echo("\nProduct List:\n")
        for product in products:
            click.echo(f"{print_product_details(product)}")
        click.echo()
    else:
        click.echo("\nFailed to retrieve products.\n")

# Define a command to get a specific product by ID.
@cli.command(help="Get a product by its ID.")
@click.option('--product-id', prompt='Please enter the Product ID', help='The ID of the product.')
def get_product(product_id):
    response = requests.get(f"{BASE_URL}/{product_id}")
    if response.status_code == 200:
        product = response.json()
        click.echo(f"\nProduct:\n\n{print_product_details(product)}\n")
    elif response.status_code == 404:
        click.echo(f"\nNo product found with ID: {product_id}\n")
    else:
        click.echo("\nFailed to retrieve product.\n")

# Define a command to search products.
@cli.command(help="Search products based on a query.")
@click.option('--query', prompt="\nPlease enter the product name, category, or ID you'd like to search for", help='The name, category, or ID of the product.')
def search_products(query):
    response = requests.get(f"{BASE_URL}/search", params={'q': query})
    
    if response.status_code == 200:
        products = response.json()
        
        if not products:
            click.echo("No products found matching the query.\n")
            return
        
        click.echo("\nSearch Results:\n")
        for product in products:
            click.echo(print_product_details(product))
        click.echo()
    else:
        click.echo(f"Error {response.status_code}: {response.text}\n")


# Define a command to add a new product.
@cli.command(help="Adds a new product to the inventory.")
@click.option('--product-id', prompt='Product ID', help='The ID of the product.')
@click.option('--product-name', prompt='Product Name', help='The name of the product.')
@click.option('--product-category', prompt='Product Category', help='The category of the product.')
@click.option('--price', prompt='Price', type=int, help='The price of the product.')
@click.option('--available-quantity', prompt='Available Quantity', type=int, help='The available quantity of the product.')
def add_product(product_id, product_name, product_category, price, available_quantity):
    product = {
        'ProductID': product_id,
        'ProductName': product_name,
        'ProductCategory': product_category,
        'Price': price,
        'AvailableQuantity': available_quantity
    }

    response = requests.post(BASE_URL, json=product)
    if response.status_code == 201:
        click.echo(f"\nProduct added successfully with ID: {product_id}\n")
    else:
        click.echo("\nFailed to add product.\n")

# Define a command to update a product.
@cli.command(help="Updates an existing product in the inventory.")
@click.option('--product-id', prompt='Product ID', help='The ID of the product to update.')
@click.option('--product-name', prompt='Product Name', help='The updated name of the product.')
@click.option('--product-category', prompt='Product Category', help='The updated category of the product.')
@click.option('--price', prompt='Price', type=int, help='The updated price of the product.')
@click.option('--available-quantity', prompt='Available Quantity', type=int, help='The updated available quantity of the product.')
def update_product(product_id, product_name, product_category, price, available_quantity):
    product = {
        'ProductName': product_name,
        'ProductCategory': product_category,
        'Price': price,
        'AvailableQuantity': available_quantity
    }

    response = requests.put(f"{BASE_URL}/{product_id}", json=product)
    if response.status_code == 200:
        click.echo(f"\nProduct {product_id} updated successfully.\n")
    else:
        click.echo("\nFailed to update product.\n")

# Define a command to delete a product.
@cli.command(help="Deletes a product from the inventory.")
@click.option('--product-id', prompt='Product ID', help='The ID of the product to delete.')
def delete_product(product_id):
    response = requests.delete(f"{BASE_URL}/{product_id}")
    if response.status_code == 200:
        click.echo(f"\nProduct {product_id} deleted successfully.\n")
    else:
        click.echo("\nFailed to delete product.\n")

if __name__ == "__main__":
    cli()