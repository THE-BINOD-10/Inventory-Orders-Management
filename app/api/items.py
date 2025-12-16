from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.security import verify_api_key
from app.api.deps import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    dependencies=[Depends(verify_api_key)]
)

# CREATE ITEM
@router.post("", response_model=ItemResponse)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    exists = db.query(Item).filter(
        Item.name == payload.name,
        Item.is_active == True
    ).first()

    if exists:
        raise HTTPException(400, "Item name already exists")

    item = Item(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        **item.__dict__,
        "low_stock": item.quantity < 5
    }


# LIST ITEMS (FILTER + PAGINATION)
@router.get("")
def list_items(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Item).filter(Item.is_active == True)

    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))

    if min_price is not None:
        query = query.filter(Item.price >= min_price)

    if max_price is not None:
        query = query.filter(Item.price <= max_price)

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }


# GET SINGLE ITEM
@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.is_active == True
    ).first()

    if not item:
        raise HTTPException(404, "Item not found")

    return {
        **item.__dict__,
        "low_stock": item.quantity < 5
    }


# UPDATE ITEM
@router.put("/{item_id}")
def update_item(item_id: int, payload: ItemCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()
    if not item:
        raise HTTPException(404, "Item not found")

    if payload.name != item.name:
        exists = db.query(Item).filter(
            Item.name == payload.name,
            Item.is_active == True
        ).first()
        if exists:
            raise HTTPException(400, "Item name already exists")

    for key, value in payload.dict().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


# SOFT DELETE
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()
    if not item:
        raise HTTPException(404, "Item not found")

    item.is_active = False
    db.commit()
    return {"message": "Item deleted successfully"}
