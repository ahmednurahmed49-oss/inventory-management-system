Inventory Management System

A Python-based inventory management system built using Flask. The application allows users to manage products, update stock information, and search for products using barcodes.

Features

* View all products in the inventory
* Add new products
* Update product details, prices, and stock quantities
* Delete products
* Search for products by barcode
* Import product information from Open Food Facts
* Validate product data and prevent duplicate barcodes
* Store inventory data in a JSON file
* Run automated tests using pytest

Technologies Used

* Python
* Flask
* Requests
* JSON
* Open Food Facts API
* Pytest

Project Structure

inventory-management-system/
├── app.py
├── cli.py
├── inventory.json
├── requirements.txt
├── services/
│   ├── __init__.py
│   └── openfoodfacts.py
└── tests/
    ├── conftest.py
    ├── test_inventory.py
    └── test_external_api.py

Installation

Clone the repository:

git clone https://github.com/ahmednurahmed49-oss/inventory-management-system.git
cd inventory-management-system

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Running the Application

Start the Flask application:

python app.py

The application runs locally at http://127.0.0.1:5000.

To use the command-line interface, open another terminal and run:

python cli.py

API Endpoints

Method	Endpoint	Description
GET	/inventory	View all products
GET	/inventory/<item_id>	View a product by ID
POST	/inventory	Add a product
PATCH	/inventory/<item_id>	Update a product
DELETE	/inventory/<item_id>	Delete a product
GET	/products/barcode/<barcode>	Search for a product by barcode
POST	/inventory/import/<barcode>	Import a product by barcode

Product Data

Each inventory product contains the following fields:

* id — unique product identifier
* name — product name
* price — product price
* stock — available quantity
* barcode — product barcode
* category — product category

Inventory data is stored in inventory.json. Product information can also be retrieved from Open Food Facts using a barcode.

Running Tests

Run the test suite with:

python -m pytest -v

Author

GitHub: ahmednurahmed49-oss