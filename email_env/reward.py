def calculate_reward(email_type, action):
    if email_type == "billing" and action == "send_to_finance":
        return 1.0

    if email_type == "technical" and action == "send_to_support":
        return 1.0

    if email_type == "general" and action == "send_to_general":
        return 1.0

    return 0.0


def grade_priority(email, action):
    correct_map = {
        "billing": "send_to_finance",
        "technical": "send_to_support",
        "general": "send_to_general"
    }

    correct_action = correct_map.get(email["email_type"])
    score = 0.0

    # correct routing
    if action == correct_action:
        score += 0.6

    # priority bonus
    if email.get("priority") == "high" and action == correct_action:
        score += 0.4

    return min(score, 1.0)