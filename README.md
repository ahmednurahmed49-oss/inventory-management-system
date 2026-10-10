Inventory Management System

Overview

This is a Flask REST API for managing inventory products. It allows users to create, view, update, and delete products. It also integrates with the Open Food Facts API to look up products by barcode and import product information into the inventory.

Features

* View all inventory products.
* Retrieve a product by its ID.
* Add new products to the inventory.
* Update product details using PATCH.
* Delete products from the inventory.
* Search for products using their barcodes.
* Import product information from an external API.
* Validate product data before creating or updating records.
* Store inventory data in a JSON file.

Technologies Used

* Python
* Flask
* REST API
* JSON
* Open Food Facts API
* Pytest
* Git and GitHub

Installation

Clone the repository and enter the project directory:

git clone https://github.com/ahmednurahmed49-oss/inventory-management-system.git
cd inventory-management-system

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Running the Application

Start the Flask development server:

python app.py

The API will usually be available at:

http://127.0.0.1:5000

API Endpoints

Method	Endpoint	Purpose
GET	/inventory	Retrieve all products
GET	/inventory/<item_id>	Retrieve a product by ID
POST	/inventory	Create a product
PATCH	/inventory/<item_id>	Update a product
DELETE	/inventory/<item_id>	Delete a product
GET	/products/barcode/<barcode>	Look up a product externally
POST	/inventory/import/<barcode>	Import a product into inventory

Example: Create a Product

Send a POST request to /inventory with JSON:

{
  "name": "Coca Cola",
  "price": 100,
  "stock": 20,
  "barcode": "5449000000996",
  "category": "Beverages"
}

Running the Tests

With the virtual environment activated, run:

python -m pytest -v

The test suite covers inventory operations, validation, barcode lookups, and product imports.

Data Storage

Inventory records are stored in inventory.json. This project uses JSON file storage rather than a database.

External API

The project uses Open Food Facts to retrieve product information by barcode. Imported products start with a price and stock quantity of zero so that these values can be entered for the local inventory.



