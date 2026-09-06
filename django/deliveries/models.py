from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Quote(models.Model):
    weight = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    postcode = models.CharField(max_length=10)
    delivery_type = models.CharField(
        max_length=8, choices=[("standard", "Standard"), ("express", "Express")]
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self) -> str:
        return f"{self.delivery_type} to {self.postcode}: £{self.cost}"
