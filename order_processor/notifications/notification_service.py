from typing import Protocol


class NotificationService(Protocol):
    def send(self, recipient: str, message: str) -> None: ...
