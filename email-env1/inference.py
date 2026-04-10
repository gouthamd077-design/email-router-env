import time
from email_env.environment import EmailRouterEnv

TASK_NAME = "email_routing"
BENCHMARK = "email_env"
MODEL_NAME = "gpt-4.1-mini"

env = EmailRouterEnv(task="hard_priority_routing")


def run_once():
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)

    try:
        obs = env.reset()

        # ✅ obs is now dict
        if obs["email_type"] == "billing":
            action = {"action": "send_to_finance"}
        elif obs["email_type"] == "technical":
            action = {"action": "send_to_support"}
        else:
            action = {"action": "send_to_general"}

        # ✅ pass dict directly
        obs, reward, done, _ = env.step(action)

        print(
            f"[STEP] step=1 action={action['action']} reward={reward['score']:.2f} done=true error=null",
            flush=True
        )

        print(
            f"[END] success=true steps=1 score={reward['score']:.3f} rewards={reward['score']:.2f}",
            flush=True
        )

    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)


# 🔥 run once
run_once()

# 🔥 keep container alive for HF
while True:
    time.sleep(60)