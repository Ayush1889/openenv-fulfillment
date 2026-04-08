import random
from .models import State, Order

class FulfillmentEnv:
    def __init__(self, seed=42):
        self.seed = seed
        random.seed(seed)
        self.reset()

    def reset(self):
        self.timestep = 0
        self.inventory = {"itemA": 10, "itemB": 8}
        self.pending_orders = self._generate_orders()
        self.completed_orders = []
        self.delayed_orders = []
        return self.state()

    def state(self):
        return State(
            timestep=self.timestep,
            inventory=self.inventory,
            pending_orders=self.pending_orders,
            completed_orders=self.completed_orders,
            delayed_orders=self.delayed_orders,
        )

    def step(self, action):
        reward = 0.0

        if action.type == "ship":
            reward += self._ship(action.payload)
        elif action.type == "restock":
            reward -= 0.2
            self.inventory[action.payload["item"]] += action.payload["qty"]
        elif action.type == "wait":
            reward -= 0.1

        self._update_deadlines()
        self.timestep += 1

        done = self.timestep >= 50
        return self.state(), reward, done, {}

    def _ship(self, payload):
        oid = payload["order_id"]
        order = next((o for o in self.pending_orders if o.order_id == oid), None)

        if not order:
            return -1.0

        for item, qty in order.items.items():
            if self.inventory.get(item, 0) < qty:
                return -0.5

        for item, qty in order.items.items():
            self.inventory[item] -= qty

        self.pending_orders.remove(order)
        self.completed_orders.append(oid)

        return 1.0 + 0.2 * order.priority

    def _update_deadlines(self):
        for o in list(self.pending_orders):
            o.deadline -= 1
            if o.deadline <= 0:
                self.pending_orders.remove(o)
                self.delayed_orders.append(o.order_id)

    def _generate_orders(self):
        return [
            Order(
                order_id=f"O{i}",
                items={"itemA": random.randint(1, 3)},
                priority=random.randint(1, 5),
                deadline=random.randint(3, 10),
            )
            for i in range(5)
        ]