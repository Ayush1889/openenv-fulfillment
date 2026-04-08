from fastapi import FastAPI
from env.environment import FulfillmentEnv
from env.models import Action

app = FastAPI()
env = FulfillmentEnv(seed=42)

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    action_obj = Action(**action)
    state, reward, done, info = env.step(action_obj)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()