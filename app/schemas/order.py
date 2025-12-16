from pydantic import BaseModel
from typing import List

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItemCreate]
