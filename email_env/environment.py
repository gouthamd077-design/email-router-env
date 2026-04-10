import random
from .models import Observation, Reward
from .tasks import TASKS


class EmailRouterEnv:

    def __init__(self, task="easy_billing_routing"):
        self.task = task
        self.state_data = None

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

    def step(self, action):
        self.state_data["step_count"] += 1

        grader = TASKS.get(self.task)
        reward_value = grader(self.state_data, action.action)

        obs = Observation(
            email_type=self.state_data["email_type"],
            priority=self.state_data["priority"]
        )

        done = True

        return obs, Reward(score=reward_value), done, {}

    def state(self):
        return self.state_data