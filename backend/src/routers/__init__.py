from routers.orders_router import orders_router
from routers.products_router import products_router
from routers.users_router import users_router


def include_routes(app):
    app.include_router(users_router)
    app.include_router(products_router)
    app.include_router(orders_router)
