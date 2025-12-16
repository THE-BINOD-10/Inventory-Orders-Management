from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    is_active: bool
    low_stock: bool
    created_at: datetime

    class Config:
        orm_mode = True
