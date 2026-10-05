import requests


def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data["product"]

        return {
            "name": product.get("product_name", "Unknown"),
            "barcode": barcode,
            "category": product.get("categories", "Unknown")
        }

    except requests.RequestException:
        return None