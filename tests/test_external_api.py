import app as inventory_app


def test_find_product_by_barcode(client, monkeypatch):
    def fake_product(barcode):
        return {
            "name": "Test Coca Cola",
            "barcode": barcode,
            "category": "Beverages",
        }

    monkeypatch.setattr(
        inventory_app, "get_product_by_barcode", fake_product
    )

    response = client.get("/products/barcode/123456789")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Test Coca Cola"


def test_find_product_not_found(client, monkeypatch):
    monkeypatch.setattr(
        inventory_app, "get_product_by_barcode", lambda barcode: None
    )

    response = client.get("/products/barcode/000000000")

    assert response.status_code == 404


def test_import_product(client, monkeypatch):
    def fake_product(barcode):
        return {
            "name": "Imported Product",
            "barcode": barcode,
            "category": "Beverages",
        }

    monkeypatch.setattr(
        inventory_app, "get_product_by_barcode", fake_product
    )

    response = client.post("/inventory/import/123456789")

    assert response.status_code == 201
    assert response.get_json()["name"] == "Imported Product"
    assert any(
        item["name"] == "Imported Product"
        for item in inventory_app.inventory
    )