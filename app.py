import json
import math
from pathlib import Path

from flask import Flask, jsonify, request
from services.openfoodfacts import get_product_by_barcode

app = Flask(__name__)

# Find inventory.json beside this Python file.
INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.json"

with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
    inventory = json.load(file)


def save_inventory():
    """Save the current inventory to the JSON file."""
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)


def next_product_id():
    """Return an ID greater than every existing product ID."""
    return max(
        (product["id"] for product in inventory),
        default=0
    ) + 1


def validate_product_data(data, partial=False):
    """Validate product fields before creating or updating a product."""
    if not isinstance(data, dict) or not data:
        return "A non-empty JSON object is required"

    allowed_fields = {"name", "price", "stock", "barcode", "category"}
    required_fields = allowed_fields

    unknown_fields = set(data.keys()) - allowed_fields
    if unknown_fields:
        return f"Unknown fields: {', '.join(sorted(unknown_fields))}"

    if not partial:
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            field = sorted(missing_fields)[0]
            return f"{field} is required"

    for field in ("name", "barcode", "category"):
        if field in data:
            value = data[field]
            if not isinstance(value, str) or not value.strip():
                return f"{field} must be a non-empty string"

    if "price" in data:
        price = data["price"]
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or not math.isfinite(price)
            or price < 0
        ):
            return "price must be a non-negative number"

    if "stock" in data:
        stock = data["stock"]
        if (
            isinstance(stock, bool)
            or not isinstance(stock, int)
            or stock < 0
        ):
            return "stock must be a non-negative integer"

    return None


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for product in inventory:
        if product["id"] == item_id:
            return jsonify(product), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/inventory", methods=["POST"])
def create_inventory():
    data = request.get_json(silent=True)
    error = validate_product_data(data)

    if error:
        return jsonify({"error": error}), 400

    product = {
        "id": next_product_id(),
        "name": data["name"].strip(),
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data["barcode"].strip(),
        "category": data["category"].strip(),
    }

    inventory.append(product)
    save_inventory()

    return jsonify(product), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json(silent=True)
    error = validate_product_data(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    for product in inventory:
        if product["id"] == item_id:
            updated_fields = data.copy()

            for field in ("name", "barcode", "category"):
                if field in updated_fields:
                    updated_fields[field] = updated_fields[field].strip()

            product.update(updated_fields)
            save_inventory()

            return jsonify(product), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for product in inventory:
        if product["id"] == item_id:
            inventory.remove(product)
            save_inventory()
            return jsonify({"message": "Product deleted"}), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/products/barcode/<barcode>", methods=["GET"])
def find_product_by_barcode(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.route("/inventory/import/<barcode>", methods=["POST"])
def import_product(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Check that the external API returned the fields we need.
    required_fields = ("name", "barcode", "category")
    if not isinstance(product, dict) or any(
        field not in product
        or not isinstance(product[field], str)
        or not product[field].strip()
        for field in required_fields
    ):
        return jsonify({"error": "External product data is incomplete"}), 502

    new_product = {
        "id": next_product_id(),
        "name": product["name"].strip(),
        "price": 0,
        "stock": 0,
        "barcode": product["barcode"].strip(),
        "category": product["category"].strip(),
    }

    inventory.append(new_product)
    save_inventory()

    return jsonify(new_product), 201


if __name__ == "__main__":
    app.run(debug=True)