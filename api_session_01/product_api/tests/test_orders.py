from product_api.extensions import db
from product_api.models import Product, Order, OrderItem
from sqlalchemy import event

def test_create_order_with_multiple_products(client, app):
    with app.app_context():
        product1 = Product(
            sku="TEST-001",
            name="Test Laptop",
            price_cents=100000,
            qty_in_stock=10
        )

        product2 = Product(
            sku="TEST-002",
            name="Test Keyboard",
            price_cents=5000,
            qty_in_stock=20
        )

        db.session.add_all([product1, product2])
        db.session.commit()

        product1_id = product1.id
        product2_id = product2.id

    response = client.post(
        "/api/v1/orders",
        json={
            "status": "pending",
            "items": [
                {
                    "product_id": product1_id,
                    "quantity": 2
                },
                {
                    "product_id": product2_id,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert len(data["items"]) == 2
    assert {
        item["product_id"] for item in data["items"]
    } == {product1_id, product2_id}

def test_list_orders_uses_eager_loading(client, app):
    with app.app_context():
        product = Product(
            sku="TEST-003",
            name="Test Mouse",
            price_cents=2000,
            qty_in_stock=30
        )

        db.session.add(product)
        db.session.flush()

        for i in range(3):
            order = Order(status="pending")

            order.items.append(
                OrderItem(
                    product=product,
                    quantity=i + 1
                )
            )

            db.session.add(order)

        db.session.commit()

        queries = []

        def count_queries(
            conn, cursor, statement, parameters, context, executemany
        ):
            if statement.lstrip().upper().startswith("SELECT"):
                queries.append(statement)

        engine = db.engine

        event.listen(
            engine,
            "before_cursor_execute",
            count_queries
        )

        try:
            response = client.get("/api/v1/orders?page=1&size=10")
        finally:
            event.remove(
                engine,
                "before_cursor_execute",
                count_queries
            )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["items"]) == 3

    for order in data["items"]:
        assert len(order["items"]) == 1

    # One SELECT for orders, one for OrderItems,
    # and one for the pagination count.
    assert len(queries) == 3