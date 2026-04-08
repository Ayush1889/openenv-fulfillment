from env.environment import FulfillmentEnv
from grader.fulfillment_grader import FulfillmentGrader
from tasks.easy import setup_easy
from tasks.medium import setup_medium
from tasks.hard import setup_hard

tasks = {
    "easy": setup_easy,
    "medium": setup_medium,
    "hard": setup_hard,
}

def run_task(name, setup):
    env = FulfillmentEnv(seed=42)
    setup(env)

    state = env.state()

    for _ in range(50):
        if state.pending_orders:
            action = {
                "type": "ship",
                "payload": {"order_id": state.pending_orders[0].order_id},
            }
        else:
            action = {"type": "wait", "payload": {}}

        state, _, done, _ = env.step(type("A", (), action))
        if done:
            break

    grader = FulfillmentGrader()
    score = grader.grade(env)
    print(f"{name}: {score:.3f}")

def main():
    for name, setup in tasks.items():
        run_task(name, setup)

if __name__ == "__main__":
    main()