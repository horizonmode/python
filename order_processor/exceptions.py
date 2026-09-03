class OrderProcessingError(Exception):
    """Base exception for the order-processing system."""


class InsufficientStockError(OrderProcessingError):
    pass


class PaymentError(OrderProcessingError):
    pass


class DuplicateOrderError(OrderProcessingError):
    pass
