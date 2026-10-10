import pytest
import app as inventory_app


@pytest.fixture
def client(monkeypatch):
    # Use fresh test data for every test.
    monkeypatch.setattr(
        inventory_app,
        "inventory",
        [
            {
                "id": 1,
                "name": "Test Product",
                "price": 100,
                "stock": 10,
                "barcode": "123456789",
                "category": "Test",
            }
        ],
    )

    # Prevent tests from modifying the real inventory file.
    monkeypatch.setattr(
        inventory_app, "save_inventory", lambda: None
    )

    return inventory_app.app.test_client()


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_inventory_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Test Product"


def test_get_inventory_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_create_inventory(client):
    product = {
        "name": "New Product",
        "price": 200,
        "stock": 20,
        "barcode": "987654321",
        "category": "Beverages",
    }

    response = client.post("/inventory", json=product)

    assert response.status_code == 201
    assert response.get_json()["name"] == "New Product"
    assert len(inventory_app.inventory) == 2


def test_create_inventory_missing_field(client):
    response = client.post(
        "/inventory",
        json={"name": "Incomplete Product"},
    )

    assert response.status_code == 400


def test_update_inventory(client):
    response = client.patch(
        "/inventory/1",
        json={"price": 250, "stock": 30},
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == 250
    assert response.get_json()["stock"] == 30


def test_update_inventory_not_found(client):
    response = client.patch(
        "/inventory/999",
        json={"price": 250},
    )

    assert response.status_code == 404


def test_delete_inventory(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200
    assert len(inventory_app.inventory) == 0


def test_delete_inventory_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
