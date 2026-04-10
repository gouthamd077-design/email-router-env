import random
from pydantic import BaseModel


# ✅ Models (required for OpenEnv)

class Observation(BaseModel):
    email_type: str
    priority: str


class Action(BaseModel):
    action: str


class Reward(BaseModel):
    score: float


# ✅ Environment

class EmailRouterEnv:

    def __init__(self, task="easy_billing_routing"):
        self.task = task
        self.state_data = None

    # ✅ RESET (FIXED - no extra fields returned)
    def reset(self):
        email_type = random.choice(["billing", "technical", "general"])
        priority = random.choice(["low", "medium", "high"])

        self.state_data = {
            "email_type": email_type,
            "priority": priority,
            "step_count": 0
        }

        return Observation(
            email_type=email_type,
            priority=priority
        )

    # ✅ STEP (OpenEnv compliant)
    def step(self, action: Action):
        self.state_data["step_count"] += 1

        correct_map = {
            "billing": "send_to_finance",
            "technical": "send_to_support",
            "general": "send_to_general"
        }

        correct_action = correct_map[self.state_data["email_type"]]

        score = 1.0 if action.action == correct_action else 0.0

        obs = Observation(
            email_type=self.state_data["email_type"],
            priority=self.state_data["priority"]
        )

        done = True

        return obs, Reward(score=score), done, {}

    # ✅ STATE (required)
    def state(self):
        return self.state_data