import random


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

        return {
            "email_type": email_type,
            "priority": priority
        }

    def step(self, action):
        self.state_data["step_count"] += 1

        correct_map = {
            "billing": "send_to_finance",
            "technical": "send_to_support",
            "general": "send_to_general"
        }

        correct_action = correct_map[self.state_data["email_type"]]

        score = 1.0 if action["action"] == correct_action else 0.0

        return (
            {
                "email_type": self.state_data["email_type"],
                "priority": self.state_data["priority"]
            },
            {"score": score},
            True,
            {}
        )

    def state(self):
        return self.state_data