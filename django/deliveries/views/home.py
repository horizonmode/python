from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.vary import vary_on_headers

from ..forms import DeliveryQuoteForm
from ..models import Quote
from ..pricing import ShippingService, calculator_for


@vary_on_headers("HX-Request")
def home(request: HttpRequest) -> HttpResponse:
    is_htmx = request.headers.get("HX-Request") == "true"
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
            if not is_htmx:
                # Normal browser submissions still use POST/Redirect/GET.
                request.session["last_quote_cost"] = str(cost)
                return redirect("home")
            form = DeliveryQuoteForm()
    else:
        form = DeliveryQuoteForm()

    # Return the same panel for success and validation errors, with HTTP 200
    # so HTMX swaps the rendered form and history into the page.
    template = "deliveries/quote_panel.html" if is_htmx else "deliveries/home.html"
    return render(request, template, {
        "title": "Get a delivery quote", "form": form, "cost": cost,
        "quotes": Quote.objects.all(),
    })
