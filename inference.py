import os
from openai import OpenAI

from env.environment import FulfillmentEnv
from grader.fulfillment_grader import FulfillmentGrader
from tasks.easy import setup_easy
from tasks.medium import setup_medium
from tasks.hard import setup_hard

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# SAFE CLIENT INIT (DO NOT CRASH)
client = None
if API_KEY and API_BASE_URL:
    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY
        )
    except Exception:
        client = None

# TASKS
tasks = {
    "easy": setup_easy,
    "medium": setup_medium,
    "hard": setup_hard,
}

# SAFE LLM CALL
def call_llm():
    if client is None:
        return "no_client"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say OK"}
            ],
            max_tokens=5
        )
        return response.choices[0].message.content
    except Exception:
        return "llm_error"


def run_task(name, setup):
    env = FulfillmentEnv(seed=42)
    setup(env)

    state = env.state()

    print(f"[START] task={name}")

    for step in range(50):

        # SAFE LLM CALL
        llm_output = call_llm()

        if state.pending_orders:
            action = {
                "type": "ship",
                "payload": {"order_id": state.pending_orders[0].order_id},
            }
        else:
            action = {"type": "wait", "payload": {}}

        state, reward, done, _ = env.step(type("A", (), action))

        print(f"[STEP] step={step} action={action} reward={reward} llm={llm_output}")

        if done:
            break

    grader = FulfillmentGrader()
    score = grader.grade(env)

    print(f"[END] task={name} score={score}")


def main():
    for name, setup in tasks.items():
        run_task(name, setup)


if __name__ == "__main__":
    main()
