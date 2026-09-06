from decimal import Decimal

from django import forms


class DeliveryQuoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "block w-full rounded-lg border border-slate-300 bg-white px-3 py-3 "
                "text-base shadow-sm focus:border-indigo-500 focus:outline-none "
                "focus:ring-2 focus:ring-indigo-200 aria-invalid:border-red-500"
            )

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
