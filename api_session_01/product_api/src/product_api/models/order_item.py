from datetime import datetime
from typing import Optional,TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order
    from .product import Product
from sqlalchemy import String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db

class OrderItem(db.Model):
    __tablename__ = "order_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )
    product_id:  Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    order: Mapped["Order"] = relationship(
        back_populates="items"
    )
    product: Mapped["Product"] = relationship(
        back_populates="order_item"
    )