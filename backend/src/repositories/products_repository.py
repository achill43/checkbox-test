from models.products import ProductSQL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, product: ProductSQL) -> ProductSQL:
        self._db.add(product)
        await self._db.commit()
        await self._db.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> ProductSQL:
        result = await self._db.execute(select(ProductSQL).filter_by(id=product_id))
        return result.scalar_one_or_none()

    async def get_list(self) -> list[ProductSQL]:
        products = await self._db.scalars(select(ProductSQL))
        return [product for product in products]
