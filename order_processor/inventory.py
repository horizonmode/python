from threading import Lock

from exceptions import InsufficientStockError
from product import Product


class Inventory:
    def __init__(self):
        self.__products: dict[str, Product] = {}
        self.__stock: dict[str, int] = {}
        self.__lock = Lock()

    def add_stock(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("product must be a Product")
        self._validate_quantity(quantity)

        with self.__lock:
            existing = self.__products.get(product.product_id)
            if existing is not None and existing != product:
                raise ValueError(f"product_id '{product.product_id}' is already in use")
            self.__products[product.product_id] = product
            self.__stock[product.product_id] = (
                self.__stock.get(product.product_id, 0) + quantity
            )

    def reserve(self, product_id: str, quantity: int) -> None:
        self._validate_quantity(quantity)
        with self.__lock:
            available = self.__stock.get(product_id, 0)
            if available < quantity:
                raise InsufficientStockError(
                    f"Product '{product_id}' has {available} available; "
                    f"{quantity} requested"
                )
            self.__stock[product_id] = available - quantity

    def release(self, product_id: str, quantity: int) -> None:
        self._validate_quantity(quantity)
        with self.__lock:
            if product_id not in self.__products:
                raise KeyError(f"Unknown product '{product_id}'")
            self.__stock[product_id] += quantity

    def get_stock(self, product_id: str) -> int:
        with self.__lock:
            return self.__stock.get(product_id, 0)

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
