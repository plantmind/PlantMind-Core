from datetime import datetime


def utc_now():
    return datetime.utcnow()


def utc_now_iso():
    return datetime.utcnow().isoformat()
