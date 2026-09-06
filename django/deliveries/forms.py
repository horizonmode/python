from decimal import Decimal

from django import forms


class DeliveryQuoteForm(forms.Form):
    weight = forms.DecimalField(
        label="Weight (kg)",
        min_value=Decimal("0.01"),
        max_digits=8,
        decimal_places=2,
    )
    postcode = forms.CharField(
        label="Destination postcode",
        max_length=10,
    )
    delivery_type = forms.ChoiceField(
        choices=[
            ("standard", "Standard"),
            ("express", "Express"),
        ]
    )
