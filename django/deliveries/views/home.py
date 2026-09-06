from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms import DeliveryQuoteForm
from ..models import Quote
from ..pricing import ShippingService, calculator_for


def home(request: HttpRequest) -> HttpResponse:
    cost = request.session.pop("last_quote_cost", None)

    if request.method == "POST":
        form = DeliveryQuoteForm(request.POST)
        if form.is_valid():
            details = form.cleaned_data
            service = ShippingService(calculator_for(details["delivery_type"]))
            cost = service.quote(details["weight"])
            Quote.objects.create(
                weight=details["weight"],
                postcode=details["postcode"],
                delivery_type=details["delivery_type"],
                cost=cost,
            )
            # Redirect after saving so refreshing does not repeat the POST.
            request.session["last_quote_cost"] = str(cost)
            return redirect("home")
    else:
        form = DeliveryQuoteForm()

    return render(request, "deliveries/home.html", {
        "title": "Get a delivery quote", "form": form, "cost": cost,
        "quotes": Quote.objects.all(),
    })
