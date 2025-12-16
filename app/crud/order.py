from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.item import Item
from app.models.order import Order
from app.models.order_item import OrderItem

def create_order(db: Session, payload):
    order = Order(customer_name=payload.customer_name)
    total = 0

    for req in payload.items:
        item = db.query(Item).filter(
            Item.id == req.item_id,
            Item.is_active == True
        ).first()

        if not item:
            raise HTTPException(404, "Item not found")

        if item.quantity < req.quantity:
            raise HTTPException(400, f"Insufficient stock for {item.name}")

        item.quantity -= req.quantity

        line_total = item.price * req.quantity
        total += line_total

        order.items.append(
            OrderItem(
                item_id=item.id,
                unit_price=item.price,
                quantity=req.quantity,
                line_total=line_total
            )
        )

    order.total_amount = total
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
