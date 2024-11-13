from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_injector import InjectorMiddleware, attach_injector
from fastapi.middleware.cors import CORSMiddleware

from injector_setup import injector_setup
from pydiator_setup import setup_pydiator

from config import settings

from db import SessionLocal, engine
from routers import include_routes


def init_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Function that handles startup and shutdown events.
        To understand more, read https://fastapi.tiangolo.com/advanced/events/
        """
        yield
        pydiator.is_ready = False  # Optional: Reset pydiator if needed
        if engine is not None:
            # Close the DB connection
            async with SessionLocal() as session:
                await session.close()

    # Ініціалізація застосунку FastAPI
    _app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, docs_url="/api/docs")

    injector = injector_setup(app=_app)
    pydiator = setup_pydiator(injector)

    # Middlewares
    _app.add_middleware(InjectorMiddleware, injector=injector)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_routes(_app)

    return _app


app = init_app()
