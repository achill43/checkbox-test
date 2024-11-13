from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from schemas.orders import OrderFilter
from models.products import OrderItemSQL, OrderSQL, PaymentSQL


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, order: OrderSQL) -> OrderSQL:
        self._db.add(order)
        await self._db.commit()
        await self._db.refresh(order)
        return order

    async def get_by_id(self, order_id: int) -> OrderSQL:
        result = await self._db.execute(
            select(OrderSQL)
            .options(
                selectinload(OrderSQL.items).selectinload(OrderItemSQL.product),
                selectinload(OrderSQL.payment),
            )
            .filter_by(id=order_id)
        )
        return result.scalar_one_or_none()

    async def get_user_orders(
        self, user_id: int, page: int, page_size: int, filters: OrderFilter
    ) -> list[OrderSQL]:
        query = (
            select(OrderSQL)
            .outerjoin(PaymentSQL, PaymentSQL.order_id == OrderSQL.id)
            .options(
                selectinload(OrderSQL.items).selectinload(OrderItemSQL.product),
                selectinload(OrderSQL.payment),
            )
            .where(OrderSQL.user_id == user_id)
        )
        if filters.created_at_from is not None:
            query = query.where(OrderSQL.created_at >= filters.created_at_from)
        if filters.created_at_to is not None:
            query = query.where(OrderSQL.created_at <= filters.created_at_to)
        if filters.payment_amount_from is not None:
            query = query.where(PaymentSQL.amount >= filters.payment_amount_from)
        if filters.payment_amount_to is not None:
            query = query.where(PaymentSQL.amount <= filters.payment_amount_to)
        if filters.payment_type is not None:
            query = query.where(PaymentSQL.type == filters.payment_type)
        result = await self._db.execute(
            query.offset((page - 1) * page_size).limit(page_size)
        )
        orders = result.unique().scalars().all()
        return [order for order in orders]
