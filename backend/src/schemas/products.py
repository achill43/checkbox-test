from decimal import Decimal

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: Decimal


class Product(BaseModel):
    id: int
    name: str
    price: Decimal

    class Config:
        from_attributes = True
