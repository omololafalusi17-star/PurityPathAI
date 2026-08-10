HIGH_RISK_PATTERNS = [
    "i am being abused",
    "someone is abusing me",
    "someone is hurting me",
    "someone is threatening me",
    "i am in immediate danger",
    "i am not safe",
    "blackmail",
    "grooming",
    "being exploited",
    "sexual exploitation",
    "forced me",
    "forcing me",
    "coercion",
    "coerced",
    "threatening to share my pictures",
    "threatening to post my pictures",
    "private pictures",
]

def assess_message(message):
    text = message.lower().strip()

    if any(pattern in text for pattern in HIGH_RISK_PATTERNS):
        return {
            "level": "high",
            "response": (
                "I'm sorry you're dealing with this. Your safety matters, and "
                "you do not have to handle a serious situation alone. If someone "
                "is threatening, hurting, pressuring, or forcing you to do something, "
                "please consider telling a trusted adult who can help, such as a parent, "
                "guardian, teacher, counselor, mentor, or another safe person. "
                "If you are in immediate danger, seek help from a safe adult or "
                "appropriate emergency service in your area. You deserve to be safe "
                "and treated with respect."
            ),
        }

    return {"level": "normal", "response": None}
