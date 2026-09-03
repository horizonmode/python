from threading import Lock


class ConsoleNotificationService:
    def __init__(self) -> None:
        self.__lock = Lock()

    def send(self, recipient: str, message: str) -> None:
        with self.__lock:
            print(f"Sending message to {recipient}: {message}")
