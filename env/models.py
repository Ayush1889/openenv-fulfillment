from pydantic import BaseModel
from typing import Dict, List

class Order(BaseModel):
    order_id: str
    items: Dict[str, int]
    priority: int
    deadline: int

class Action(BaseModel):
    type: str
    payload: Dict

class State(BaseModel):
    timestep: int
    inventory: Dict[str, int]
    pending_orders: List[Order]
    completed_orders: List[str]
    delayed_orders: List[str]