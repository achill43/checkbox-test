import injector
from fastapi_injector import request_scope
from sqlalchemy.ext.asyncio.session import AsyncSession

from request_context import RequestContextProvider
from repositories.order_repository import OrderRepository
from repositories.order_item_repository import OrderItemRepository
from repositories.payment_repository import PaymentRepository
from repositories.products_repository import ProductRepository
from repositories.user_repository import UserRepository

from db import SessionLocal
from config import Settings, settings


def configure_for_production(binder: injector.Binder) -> None:
    binder.bind(Settings, to=settings)


class CoreModule(injector.Module):
    @injector.provider
    @request_scope
    def get_request_context(self) -> RequestContextProvider:
        return RequestContextProvider()

    @injector.provider
    @request_scope
    def get_session(self) -> AsyncSession:
        return SessionLocal()

    @injector.provider
    @request_scope
    def get_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @injector.provider
    @request_scope
    def get_product_repo(self, session: AsyncSession) -> ProductRepository:
        return ProductRepository(session)

    @injector.provider
    @request_scope
    def get_order_repo(self, session: AsyncSession) -> OrderRepository:
        return OrderRepository(session)

    @injector.provider
    @request_scope
    def get_order_item_repo(self, session: AsyncSession) -> OrderItemRepository:
        return OrderItemRepository(session)

    @injector.provider
    @request_scope
    def get_payment_repo(self, session: AsyncSession) -> PaymentRepository:
        return PaymentRepository(session)
