def is_empty(value):
    return value is None or value == ""


def has_value(value):
    return not is_empty(value)
