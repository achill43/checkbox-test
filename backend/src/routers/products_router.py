from fastapi import APIRouter, status
from pydiator_core.mediatr import pydiator
from use_cases.products.create_product import (CreateProductRequest,
                                               CreateProductResponse)
from use_cases.products.get_products_list import (GetProductsListRequest,
                                                  GetProductsListResponse)

products_router = APIRouter(prefix="/products")


@products_router.post(
    "/",
    summary="Create new product",
    responses={
        status.HTTP_200_OK: {"model": CreateProductResponse},
    },
)
async def create_product(req: CreateProductRequest):
    return await pydiator.send(req=req)


@products_router.get(
    "/",
    summary="Get products list",
    responses={
        status.HTTP_200_OK: {"model": GetProductsListResponse},
    },
)
async def get_products_list():
    return await pydiator.send(req=GetProductsListRequest())
