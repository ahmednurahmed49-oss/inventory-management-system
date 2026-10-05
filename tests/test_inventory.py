from app import app


def test_get_inventory():
    client = app.test_client()

    response = client.get("/inventory")


    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_inventory():
    client = app.test_client()

    product = {
        "name": "Test Product",
        "price": 100,
        "stock": 10,
        "barcode": "123456789",
        "category": "Test"
    }
    response = client.post("/inventory", json=product)

    assert response.status_code == 201
    assert response.get_json()["name"] == "Test Product"

def test_update_inventory():
    client = app.test_client()

    product = {
        "name": "Update Test",
        "price": 100,
        "stock": 10,
        "barcode": "987654321",
        "category": "Test",
    }

    create_response = client.post("/inventory", json=product) 
    product_id = create_response.get_json()["id"]


    response = client.patch(
        f"/inventory/{product_id}",
        json={"price": 200, "stock": 20}
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == 200
    assert response.get_json()["stock"] == 20

def test_delete_inventory():
    client = app.test_client()


    product = {
        "name": "Delete Test",
        "price": 100,
        "stock": 10,
        "barcode": "11111111",
        "category": "Test",

    }

    create_response = client.post("/inventory", json=product)
    product_id = create_response.get_json()["id"]


    response = client.delete(f"/inventory/{product_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Product deleted"

def test_get_inventory_item_not_found():
    client = app.test_client()

    response = client.get("/inventory/999999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"

