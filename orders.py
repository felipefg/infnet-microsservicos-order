from enum import Enum
from typing import List

from uuid import UUID, uuid4

from pydantic import BaseModel


class OrderStatus(str, Enum):
    created = 'created'
    approved = 'approved'
    cancelled = 'cancelled'
    done = 'done'


class Order(BaseModel):
    order_id: UUID
    client_id: int
    item_ids: List[int]
    status: OrderStatus = OrderStatus.created


ORDERS = {}


def create_order(client_id: int, item_ids: List[int]):
    """Create a new order object and save it to the database
    """
    order = Order(
        order_id=uuid4(),
        client_id=client_id,
        item_ids=item_ids,
    )
    ORDERS[str(order.order_id)] = order
    return order


def get_order(order_id: str):
    return ORDERS.get(order_id)
