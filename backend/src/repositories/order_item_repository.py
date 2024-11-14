from models.products import OrderItemSQL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, order_item: OrderItemSQL) -> OrderItemSQL:
        self._db.add(order_item)
        await self._db.commit()
        await self._db.refresh(order_item)
        return order_item

    async def get_by_id(self, id: int) -> OrderItemSQL:
        result = await self._db.execute(select(OrderItemSQL).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: int) -> list[OrderItemSQL]:
        order_items = await self._db.scalars(
            select(OrderItemSQL).where(OrderItemSQL.order_id == order_id)
        )
        return [order_item for order_item in order_items]

    async def bulk_create(self, order_items: list[OrderItemSQL]) -> None:
        self._db.add_all(order_items)

        await self._db.commit()
