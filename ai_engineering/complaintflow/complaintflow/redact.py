import re


EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{7,}\d)(?!\d)")
ACCOUNT = re.compile(r"\b(?:account|acct|card|loan)[\s:#-]*\d{4,}\b", re.I)


def redact(text: str) -> str:
    """Remove common direct identifiers before text reaches a model/provider."""
    value = EMAIL.sub("[REDACTED_EMAIL]", text)
    value = PHONE.sub("[REDACTED_PHONE]", value)
    return ACCOUNT.sub("[REDACTED_ACCOUNT]", value)

