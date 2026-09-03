from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationJob:
    recipient: str
    message: str
