import pytest
import app as inventory_app


@pytest.fixture
def client(monkeypatch):
    test_inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "price": 100,
            "stock": 10,
            "barcode": "123456789",
            "category": "Test"
        }
    ]

    monkeypatch.setattr(
        inventory_app, "inventory", test_inventory
    )

    monkeypatch.setattr(
        inventory_app, "save_inventory", lambda: None
    )

    return inventory_app.app.test_client()
