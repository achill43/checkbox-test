from datetime import date
from decimal import Decimal

from models.products import PaymentType
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItem(BaseModel):
    id: int
    name: str
    price: Decimal
    quantity: int
    total: Decimal

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    type: PaymentType


class Payment(BaseModel):
    id: int
    type: PaymentType
    amount: Decimal

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    products: list[OrderItemCreate]
    payment: PaymentCreate
    total: Decimal


class Order(BaseModel):
    id: int
    products: list[OrderItem]
    payment: Payment
    total: Decimal
    rest: Decimal
    created_at: date

    class Config:
        from_attributes = True


class OrderFilter(BaseModel):
    created_at_from: date | None = None
    created_at_to: date | None = None
    payment_type: PaymentType | None = None
    payment_amount_from: Decimal | None = None
    payment_amount_to: Decimal | None = None
