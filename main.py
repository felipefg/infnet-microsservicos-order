from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import List

import orders
import producer

app = FastAPI()


class CreateOrderRequest(BaseModel):
    client_id: int
    item_ids: List[int]


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/order", response_model=orders.Order)
async def create_order(order_req: CreateOrderRequest):
    order = orders.create_order(**order_req.dict())

    producer.emit_order_created(order)

    return order


@app.get("/order/{order_id}", response_model=orders.Order)
async def get_order(order_id: str):
    print(orders.ORDERS)
    order = orders.get_order(order_id=order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


class UpdateOrderRequest(BaseModel):
    status: orders.OrderStatus


@app.put("/order/{order_id}/status")
async def update_order(order_id: str, new_status_req: UpdateOrderRequest):

    order = orders.get_order(order_id=order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = new_status_req.status

    if order.status == orders.OrderStatus.cancelled:
        producer.emit_order_cancelled(order)

    return order
