import os
import json
from openai import OpenAI
from email_env.environment import EmailRouterEnv
from email_env.models import Action

# ✅ Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = "gpt-4.1-mini"

env = EmailRouterEnv(task="hard_priority_routing")

print(f"[START] task=email_routing env=email_env model={MODEL_NAME}")

rewards = []
steps = 0


def get_llm_action(obs):
    """Single safe OpenAI call"""

    prompt = f"""
    Email type: {obs.email_type}
    Priority: {obs.priority}

    Choose one action:
    send_to_finance
    send_to_support
    send_to_general

    Return ONLY JSON:
    {{"action": "..."}}
    """

    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = res.choices[0].message.content.strip()

        # ✅ Handle markdown JSON
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except Exception as e:
        # ✅ Fallback (VERY IMPORTANT)
        print(f"[DEBUG] OpenAI error: {str(e)}")
        return {"action": "send_to_general"}


try:
    obs = env.reset()

    # ✅ ONLY ONE API CALL (low cost)
    action_dict = get_llm_action(obs)

    action = Action(**action_dict)

    obs, reward, done, _ = env.step(action)

    steps += 1
    rewards.append(reward.score)

    print(
        f"[STEP] step={steps} action={action.action} reward={reward.score:.2f} done=true error=null"
    )

    score = reward.score
    success = score > 0.5

except Exception as e:
    success = False
    score = 0.0
    print(f"[STEP] step={steps} action=null reward=0.00 done=true error={str(e)}")

print(
    f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={','.join(f'{r:.2f}' for r in rewards)}"
)