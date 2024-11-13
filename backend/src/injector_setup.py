from fastapi import FastAPI
from fastapi_injector import attach_injector
from injector import Injector

from module import CoreModule, configure_for_production


def injector_setup(app: FastAPI):
    injector = Injector(
        [
            configure_for_production,
            CoreModule,
        ]
    )
    attach_injector(app, injector)
    return injector
