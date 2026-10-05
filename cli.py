import requests

BASE_URL = "http://127.0.0.1:5000"
def view_inventory():
 
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        products = response.json()

        if not products:
            print("Inventory is empty.")
            return

        print("\n--- Inventory ---")

        for product in products:
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"Stock: {product['stock']}")
            print(f"Barcode: {product['barcode']}")
            print(f"Category: {product['category']}")
            print("-----------------")

    else:
        print("Failed to retrieve inventory.")

def add_inventory():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock: "))
    barcode = input("Enter barcode: ")
    category = input("Enter category: ")

    product = {
        "name": name,
        "price": price,
        "stock": stock,
        "barcode": barcode,
        "category": category
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=product
    )

    if response.status_code == 201:
        print("\nProduct added successfully!")
        print(response.json())
    else:
        print("\nFailed to add product.")
        print(response.json())

def update_inventory():
    item_id = int(input("Enter product ID: "))
    price = float(input("Enter new price: "))
    stock = int(input("Enter new stock: "))

    data = {
        "price": price,
        "stock": stock
    }

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("\nProduct updated successfully!")
        print(response.json())
    elif response.status_code == 404:
        print("\nProduct not found.")
    else:
        print("\nFailed to update product.")

def delete_inventory():
    item_id = int(input("Enter product ID to delete: "))

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("\nProduct deleted successfully!")
        print(response.json())
    elif response.status_code == 404:
        print("\nProduct not found.")
    else:
        print("\nFailed to delete product.")


def find_product():
    barcode = input("Enter product barcode: ")

    response = requests.get(
        f"{BASE_URL}/products/barcode/{barcode}"
    )

    if response.status_code == 200:
        print("\nProduct found!")
        print(response.json())
    elif response.status_code == 404:
        print("\nProduct not found.")
    else:
        print("\nFailed to find product.")

def main():
    while True:
        print("\n--- Inventory Management System ---")
        print("1. View inventory")
        print("2. Add product")
        print("3. Update product")
        print("4. Delete product")
        print("5. Find product by barcode")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_inventory()
        elif choice == "3":
            update_inventory()
        elif choice == "4":
            delete_inventory()
        elif choice == "5":
            find_product()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()