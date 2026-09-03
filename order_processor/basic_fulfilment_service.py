from time import sleep

from order import Order


class BasicFulfilmentService:
    def __init__(self, processing_delay: float = 0.02):
        if processing_delay < 0:
            raise ValueError("processing_delay cannot be negative")
        self.__processing_delay = processing_delay

    def fulfil(self, order: Order) -> None:
        # A real implementation could call a warehouse or shipping API.
        sleep(self.__processing_delay)
