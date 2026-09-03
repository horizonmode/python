from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING_PAYMENT = "processing_payment"
    PAID = "paid"
    FULFILLING = "fulfilling"
    COMPLETED = "completed"
    FAILED = "failed"
