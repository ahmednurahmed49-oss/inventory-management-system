from app import app


def test_find_product_by_barcode(monkeypatch):
    client = app.test_client()

    def fake_product(barcode):
        return {
            "name": "Test Coca Cola",
            "barcode": barcode,
            "category": "Beverages"
        }

    monkeypatch.setattr("app.get_product_by_barcode", fake_product)

    response = client.get("/products/barcode/123456789")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Test Coca Cola"