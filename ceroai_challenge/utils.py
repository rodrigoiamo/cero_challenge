from datetime import datetime


def compute_delta_days_from_now(date: datetime) -> int:
    return (date - datetime.now()).days


def from_iso_format(date: str) -> datetime:
    return datetime.fromisoformat(date)
