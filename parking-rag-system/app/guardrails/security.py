BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "database password"
]


def detect_prompt_injection(user_input: str):

    lower_input = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in lower_input:
            return True

    return False