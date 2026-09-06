from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from ..models import Quote


@require_safe
def quote_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve one quote with GET (or HEAD), without changing it."""
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, "deliveries/quote_detail.html", {"quote": quote})
