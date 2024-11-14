from typing import cast

from depends.auth_deps import get_current_user
from fastapi import APIRouter, Depends, Response, status
from pydiator_core.mediatr import pydiator
from schemas.users import UserResponse
from use_cases.checks.generate_check import (GenerateCheckRequest,
                                             GenerateCheckResponse)
from use_cases.orders.create_order import (CreateOrderRequest,
                                           CreateOrderResponse)
from use_cases.orders.get_user_orders import (GetUserOrdersRequest,
                                              GetUserOrdersResponse)

orders_router = APIRouter(prefix="/orders")


@orders_router.post(
    "/",
    summary="Create new order",
    responses={
        status.HTTP_200_OK: {"model": CreateOrderResponse},
    },
)
async def create_product(
    req: CreateOrderRequest, user: UserResponse = Depends(get_current_user)
):
    return await pydiator.send(req=req)


@orders_router.get(
    "/my",
    summary="Get user's orders list",
    responses={
        status.HTTP_200_OK: {"model": GetUserOrdersResponse},
    },
)
async def get_user_order(
    req: GetUserOrdersRequest = Depends(GetUserOrdersRequest),
    user: UserResponse = Depends(get_current_user),
):
    return await pydiator.send(req=req)


@orders_router.get(
    "/check/{:id}",
    summary="Get user's orders list",
)
async def generate_check(id: int):
    responce = cast(
        GenerateCheckResponse, await pydiator.send(req=GenerateCheckRequest(id=id))
    )
    response_route = Response(
        content=responce.html_content,
        media_type="text/html",
        headers={
            "Content-Disposition": "attachment;filename=check.html",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
    return response_route
