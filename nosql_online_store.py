import pymongo
import re

# ============================================================

def is_empty_string(value) -> bool:
    return isinstance(value, str) and value.strip() == ""


def validate_email(email: str) -> bool:
    if not isinstance(email, str) or is_empty_string(email):
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False

    username, domain = parts
    if is_empty_string(username) or is_empty_string(domain):
        return False

    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False

    for part in domain.split("."):
        if is_empty_string(part):
            return False

    return True


def validate_phone(phone: str) -> bool:
    if not isinstance(phone, str) or is_empty_string(phone):
        return False

    if not re.fullmatch(r"[\d\s\-\(\)]+", phone):
        return False

    digits = re.findall(r"\d", phone)
    return len(digits) >= 7


# ============================================================
# DB CONNECTION
# ============================================================

def connect(host, port, timeout):
    try:
        client = pymongo.MongoClient(host, port, serverSelectionTimeoutMS=timeout)
        client.server_info()
        return client
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_database(client):
    db = client["online_store"]
    products_collection = db["products"]
    customers_collection = db["customers"]
    orders_collection = db["orders"]
    return db, products_collection, customers_collection, orders_collection


# ============================================================
# PRODUCTS
# ============================================================

def add_product(products_collection, product_id, name, price, stock, category):
    if products_collection.find_one({"product_id": product_id}):
        print(f"Error: product_id {product_id} already exists!")
        return None

    fields = {
        "product_id": str,
        "name": str,
        "price": (int, float),
        "stock": int,
        "category": str
    }

    values = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "category": category
    }

    for field_name, expected_type in fields.items():
        if not isinstance(values[field_name], expected_type):
            print(f"Field {field_name} should be of type {expected_type}")
            return None

    for field_name in ("product_id", "name", "category"):
        if is_empty_string(values[field_name]):
            print(f"Error: Field '{field_name}' cannot be empty or whitespace.")
            return None

    print(f"Added product with id {product_id}")
    return products_collection.insert_one(values)


def view_product(products_collection, product_id):
    product = products_collection.find_one({"product_id": product_id})
    if product:
        print(f"Product found: {product}")
        return product
    print(f"No product with product_id {product_id}")
    return None


def view_all_products(products_collection):
    print("All products:")
    products = list(products_collection.find())
    for product in products:
        print(product)
    return products


def update_product(products_collection, product_id, **updates):
    if not products_collection.find_one({"product_id": product_id}):
        print(f"Error: no product with product_id {product_id}!")
        return None

    fields = {"name": str, "price": (int, float), "stock": int, "category": str}

    for field_name, value in updates.items():
        if field_name not in fields:
            print(f"Field {field_name} is not a valid field for update.")
            return None

        expected_type = fields[field_name]
        if not isinstance(value, expected_type):
            print(f"Error: wrong data type for field '{field_name}' in update_product.")
            return None

        if field_name in ("name", "category") and is_empty_string(value):
            print(f"Error: Field '{field_name}' cannot be empty or whitespace.")
            return None

    result = products_collection.update_one({"product_id": product_id}, {"$set": updates})
    if result.modified_count:
        print(f"Updated product {product_id} with updates: {updates}")
    else:
        print(f"No changes made to {product_id}")
    return result


def delete_product(products_collection, product_id):
    product = products_collection.find_one({"product_id": product_id})
    if not product:
        print(f"No product with product_id {product_id}")
        return None
    print(f"Deleting product with product_id {product_id}")
    return products_collection.delete_one({"product_id": product_id})


# ============================================================
# CUSTOMERS
# ============================================================

def add_customer(customers_collection, customer_id, name, email, phone, address):
    if customers_collection.find_one({"customer_id": customer_id}):
        print(f"Error: customer_id {customer_id} already exists!")
        return None

    fields = {"customer_id": str, "name": str, "email": str, "phone": str, "address": str}
    values = {"customer_id": customer_id, "name": name, "email": email, "phone": phone, "address": address}

    for field_name, expected_type in fields.items():
        if not isinstance(values[field_name], expected_type):
            print(f"Field {field_name} should be of type {expected_type}")
            return None

    for field_name, value in values.items():
        if is_empty_string(value):
            print(f"Error: Field '{field_name}' cannot be empty or whitespace.")
            return None

    if not validate_email(email):
        print(f"Error: Invalid email format '{email}'.")
        return None

    if not validate_phone(phone):
        print(f"Error: Invalid phone format '{phone}'. Must contain >= 7 digits; allowed: digits/spaces/-/().")
        return None

    print(f"Added customer with id {customer_id}")
    return customers_collection.insert_one(values)


def view_customer(customers_collection, customer_id):
    customer = customers_collection.find_one({"customer_id": customer_id})
    if customer:
        print(f"Customer found: {customer}")
        return customer
    print(f"No customer with customer_id {customer_id}")
    return None


def view_all_customers(customers_collection):
    print("All customers:")
    customers = list(customers_collection.find())
    for customer in customers:
        print(customer)
    return customers


def update_customer(customers_collection, customer_id, **updates):
    if not customers_collection.find_one({"customer_id": customer_id}):
        print(f"Error: no customer with customer_id {customer_id}!")
        return None

    fields = {"name": str, "email": str, "phone": str, "address": str}

    for field_name, value in updates.items():
        if field_name not in fields:
            print(f"Field {field_name} is not a valid field for update.")
            return None

        if not isinstance(value, fields[field_name]):
            print(f"Error: wrong data type for field '{field_name}' in update_customer.")
            return None

        if is_empty_string(value):
            print(f"Error: Field '{field_name}' cannot be empty or whitespace.")
            return None

        if field_name == "email" and not validate_email(value):
            print(f"Error: Invalid email format '{value}'.")
            return None

        if field_name == "phone" and not validate_phone(value):
            print(f"Error: Invalid phone format '{value}'.")
            return None

    result = customers_collection.update_one({"customer_id": customer_id}, {"$set": updates})
    if result.modified_count:
        print(f"Updated customer {customer_id} with updates: {updates}")
    else:
        print(f"No changes made to {customer_id}")
    return result


def delete_customer(customers_collection, customer_id):
    customer = customers_collection.find_one({"customer_id": customer_id})
    if not customer:
        print(f"No customer with customer_id {customer_id}")
        return None
    print(f"Deleting customer with customer_id {customer_id}")
    return customers_collection.delete_one({"customer_id": customer_id})


# ============================================================
# ORDERS
# orders: _id, order_id, customer_id, items[{product_id, quantity, price}], total_price
# ============================================================

def add_order(orders_collection, order_id, customer_id, items, total_price=None):
    if orders_collection.find_one({"order_id": order_id}):
        print(f"Error: order_id {order_id} already exists!")
        return None

    if not isinstance(order_id, str) or is_empty_string(order_id):
        print("Error: Field 'order_id' must be a non-empty string.")
        return None
    if not isinstance(customer_id, str) or is_empty_string(customer_id):
        print("Error: Field 'customer_id' must be a non-empty string.")
        return None

    if not isinstance(items, list) or len(items) == 0:
        print("Error: 'items' must be a non-empty list.")
        return None

    computed_total = 0.0
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            print(f"Error: item #{idx} must be a dict.")
            return None

        for key in ("product_id", "quantity", "price"):
            if key not in item:
                print(f"Error: item #{idx} missing key '{key}'.")
                return None

        if not isinstance(item["product_id"], str) or is_empty_string(item["product_id"]):
            print(f"Error: item #{idx} 'product_id' cannot be empty or whitespace.")
            return None

        if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
            print(f"Error: item #{idx} 'quantity' must be int > 0.")
            return None

        if not isinstance(item["price"], (int, float)) or float(item["price"]) < 0:
            print(f"Error: item #{idx} 'price' must be number >= 0.")
            return None

        computed_total += item["quantity"] * float(item["price"])

    if total_price is None:
        total_price = computed_total
    else:
        if not isinstance(total_price, (int, float)):
            print("Error: 'total_price' must be a number.")
            return None
        if abs(float(total_price) - computed_total) > 0.01:
            print(f"Error: total_price ({total_price}) != sum(items) ({computed_total:.2f}).")
            return None

    order_doc = {
        "order_id": order_id,
        "customer_id": customer_id,
        "items": items,
        "total_price": float(total_price)
    }

    print(f"Added order with id {order_id}")
    return orders_collection.insert_one(order_doc)


def view_orders_by_customer(orders_collection, customer_id):
    if not isinstance(customer_id, str) or is_empty_string(customer_id):
        print("Error: customer_id must be a non-empty string.")
        return []

    orders = list(orders_collection.find({"customer_id": customer_id}))
    if not orders:
        print(f"No orders found for customer {customer_id}")
        return []

    print(f"--- Orders for customer {customer_id} ---")
    for order in orders:
        print(f"Order ID: {order.get('order_id')}")
        print(f"  Items: {order.get('items')}")
        print(f"  Total Price: {order.get('total_price'):.2f}")
        print()
    return orders


# ============================================================
# AGGREGATIONS
# ============================================================

def count_orders_per_customer(orders_collection):
    print("\n--- Number of orders per customer ---")
    pipeline = [
        {"$group": {"_id": "$customer_id", "order_count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = list(orders_collection.aggregate(pipeline))
    if not results:
        print("No orders found in the database.")
        return []
    for r in results:
        print(f"{r['_id']}: {r['order_count']}")
    return results


def total_spent_per_customer(orders_collection):
    print("\n--- Total money spent per customer ---")
    pipeline = [
        {"$group": {"_id": "$customer_id", "total_spent": {"$sum": "$total_price"}}},
        {"$sort": {"_id": 1}}
    ]
    results = list(orders_collection.aggregate(pipeline))
    if not results:
        print("No orders found in the database.")
        return []
    for r in results:
        print(f"{r['_id']}: {r['total_spent']:.2f}")
    return results


# ============================================================
# MAIN + TESTS
# ============================================================

def main():
    client = connect("localhost", 27017, 1000)
    if client is None:
        print("Quitting...")
        return

    db, products_collection, customers_collection, orders_collection = create_database(client)

    products_collection.delete_many({})
    customers_collection.delete_many({})
    orders_collection.delete_many({})

    print("=== PRODUCTS TESTS ===")
    add_product(products_collection, "P00001", "Keyboard", 499.99, 10, "Peripherals")
    add_product(products_collection, "P00002", "Mouse", 199.99, 20, "Peripherals")

    add_product(products_collection, " ", "Bad", 1.0, 1, "Cat")
    update_product(products_collection, "P00001", name=" ")

    print("\n=== CUSTOMERS TESTS ===")
    add_customer(customers_collection, "Customer01", "Jan Kowalski", "jan@firma.pl", "123-456-789", "Warsaw, Poland")
    add_customer(customers_collection, "Customer02", "Anna Nowak", "anna@firma.pl", "(987) 654-321", "Krakow, Poland")
    add_customer(customers_collection, "Customer03", "Piotr Wisniewski", "piotr@firma.pl", "555 666 777", "Wroclaw, Poland")

    add_customer(customers_collection, "Customer04", " ", "x@firma.pl", "1234567", "Addr")
    add_customer(customers_collection, "Customer05", "Bad Email", "bademail", "1234567", "Addr")
    add_customer(customers_collection, "Customer06", "Bad Phone", "ok@firma.pl", "12-34", "Addr")
    add_customer(customers_collection, "Customer07", "Bad Char", "ok2@firma.pl", "+48 123-456-789", "Addr")

    update_customer(customers_collection, "Customer01", email="nowy@firma.pl")
    update_customer(customers_collection, "Customer01", phone="(111) 222-333")
    update_customer(customers_collection, "Customer01", email="invalid@domain")

    print("\n=== ORDERS TESTS ===")
    add_order(
        orders_collection,
        "O001",
        "Customer01",
        items=[
            {"product_id": "P00001", "quantity": 2, "price": 100.00},
        ]
    )

    add_order(
        orders_collection,
        "O002",
        "Customer01",
        items=[
            {"product_id": "P00002", "quantity": 5, "price": 65.00},
        ]
    )

    add_order(
        orders_collection,
        "O003",
        "Customer03",
        items=[
            {"product_id": "P00002", "quantity": 2, "price": 87.50},
        ]
    )

    add_order(orders_collection, " ", "Customer01", items=[{"product_id": "P00001", "quantity": 1, "price": 10.0}])
    add_order(orders_collection, "O004", " ", items=[{"product_id": "P00001", "quantity": 1, "price": 10.0}])

    print("\n=== view_orders_by_customer ===")
    view_orders_by_customer(orders_collection, "Customer01")
    view_orders_by_customer(orders_collection, "Customer02")
    view_orders_by_customer(orders_collection, "Customer03")

    print("\n=== AGGREGATIONS ===")
    count_orders_per_customer(orders_collection)
    total_spent_per_customer(orders_collection)

    client.close()


if __name__ == "__main__":
    main()
