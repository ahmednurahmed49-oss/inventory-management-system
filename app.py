import json

from flask import Flask, jsonify, request
from services.openfoodfacts import get_product_by_barcode

app = Flask(__name__)

with open("inventory.json", "r") as file:
    inventory = json.load(file)


def save_inventory():
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for product in inventory:
        if product["id"] == item_id:
            return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    for product in inventory:
        if product ["id"] == item_id:
            if "name" in data:
                product["name"] = data["name"]

            if "price" in data:
                product["price"] = data["price"]

            if "stock" in data:
                product["stock"] = data["stock"]

            if "barcode" in data:
                product["barcode"] = data["barcode"]

            if "category" in data:
                product["category"] = data["category"]

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

    new_product = {
        "id": len(inventory) + 1,
        "name": product["name"],
        "price": 0,
        "stock": 0,
        "barcode": product["barcode"],
        "category": product["category"]
    }

    inventory.append(new_product)
    save_inventory()

    return jsonify(new_product), 201




@app.route("/inventory", methods=["POST"])
def create_inventory():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["name", "price", "stock", "barcode", "category"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    product = {
        "id": len(inventory) + 1,
        "name": data["name"],
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data["barcode"],
        "category": data["category"],
}

    inventory.append(product)
    save_inventory()

    return jsonify(product), 201


if __name__ == "__main__":
    app.run(debug=True)