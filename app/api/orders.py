from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.security import verify_api_key
from app.api.deps import get_db
from app.schemas.order import OrderCreate
from app.crud.order import create_order
from app.models.order import Order

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(verify_api_key)]
)

# CREATE ORDER
@router.post("")
def create_order_api(payload: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, payload)


# GET ORDER BY ID
@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    return order


# LIST ORDERS WITH FILTERS
@router.get("")
def list_orders(
    customer_name: str | None = None,
    status: str | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Order)

    if customer_name:
        query = query.filter(Order.customer_name.ilike(f"%{customer_name}%"))

    if status:
        query = query.filter(Order.status == status)

    if from_date:
        query = query.filter(Order.created_at >= from_date)

    if to_date:
        query = query.filter(Order.created_at <= to_date)

    total = query.count()
    orders = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "orders": orders,
        "total": total,
        "page": page,
        "page_size": page_size
    }


# CANCEL ORDER (OPTIONAL BUT BONUS)
@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")

    if order.status == "cancelled":
        raise HTTPException(400, "Order already cancelled")

    order.status = "cancelled"
    db.commit()
    return {"message": "Order cancelled"}
