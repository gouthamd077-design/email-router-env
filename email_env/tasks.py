from .reward import grade_priority


def grade_billing(email, action):
    return 1.0 if (
        email["email_type"] == "billing"
        and action == "send_to_finance"
    ) else 0.0


def grade_technical(email, action):
    return 1.0 if (
        email["email_type"] == "technical"
        and action == "send_to_support"
    ) else 0.0


TASKS = {
    "easy_billing_routing": grade_billing,
    "medium_technical_routing": grade_technical,
    "hard_priority_routing": grade_priority
}