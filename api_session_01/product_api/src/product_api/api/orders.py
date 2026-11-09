from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from ..extensions import db
from ..models import Product, OrderItem, Order
from .errors import Conflict
from .schemas import *

orders_bp = Blueprint(
    "orders", __name__, url_prefix="/api/v1/orders"
)

@orders_bp.post("")
def create_order():
    body = OrderIn().load(request.json)
    items_data = body.pop("items")

    product_ids = {
        item["product_id"] for item in items_data
    }

    products = db.session.scalars(
        db.select(Product).where(
            Product.id.in_(product_ids)
        )
    ).all()

    products_by_id = {
        product.id: product for product in products
    }

    missing_ids = product_ids - products_by_id.keys()

    if missing_ids:
        abort(
            404,
            description=f"Products not found: {sorted(missing_ids)}"
        )

    order = Order(**body)

    for item_data in items_data:
        order_item = OrderItem(
            product=products_by_id[item_data["product_id"]],
            quantity=item_data["quantity"]
        )
        order.items.append(order_item)

    db.session.add(order)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="Could not create order")

    return OrderOut().dump(order), 201

@orders_bp.get("")
def list_orders():
    page = max(1, int(request.args.get("page", 1)))
    size = min(100, max(1, 
                        int(request.args.get("size", 200))))
    stmt = (
        db.select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.id)
        .offset((page-1) * size).limit(size)
    )
    orders = db.session.scalars(stmt).all()
    total = db.session.scalar(
        db.select(db.func.count()).select_from(Order)
    )

    return {
        "items": OrderOut(many=True).dump(orders),
        "page": page,
        "size": size,
        "total": total
    }, 200
