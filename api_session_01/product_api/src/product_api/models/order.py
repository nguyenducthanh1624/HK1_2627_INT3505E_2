from datetime import datetime
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .order_item import OrderItem
from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db

class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

    items: Mapped[list["OrderItem"]] = relationship(
            back_populates="order"
    )

    created_at: Mapped[datetime] = mapped_column(
            DateTime, server_default=func.now(), nullable=False
        )
    status: Mapped[Optional[str]] = mapped_column(String(100))

