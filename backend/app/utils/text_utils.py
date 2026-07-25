def normalize_text(text: str) -> str:
    return text.strip().lower()


def is_blank(text: str) -> bool:
    return len(text.strip()) == 0
