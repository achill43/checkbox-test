from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.products import PaymentSQL


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, payment: PaymentSQL) -> PaymentSQL:
        self._db.add(payment)
        await self._db.commit()
        await self._db.refresh(payment)
        return payment

    async def get_by_id(self, id: int) -> PaymentSQL | None:
        result = await self._db.execute(select(PaymentSQL).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: int) -> list[PaymentSQL]:
        payments = await self._db.scalars(
            select(PaymentSQL).where(PaymentSQL.order_id == order_id)
        )
        return [payment for payment in payments]
