from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Quote


class QuoteFlowTests(TestCase):
    def test_quote_detail(self):
        quote = Quote.objects.create(
            weight=Decimal("3"),
            postcode="SW1A 1AA",
            delivery_type="standard",
            cost=Decimal("6"),
        )
        url = reverse("quote_detail", args=[quote.pk])
        response = self.client.get(url)
        self.assertContains(response, "SW1A 1AA")
        self.assertContains(response, "£6.00")
        self.assertEqual(response.context["quote"], quote)
        self.assertContains(self.client.get(reverse("home")), f'href="{url}"')
        self.assertEqual(self.client.head(url).status_code, 200)
        for method in (
            self.client.post,
            self.client.put,
            self.client.patch,
            self.client.delete,
        ):
            self.assertEqual(method(url).status_code, 405)
        self.assertEqual(Quote.objects.count(), 1)

    def test_missing_quote_returns_404(self):
        response = self.client.get(reverse("quote_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_empty_history(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No quotes yet.")

    def test_history_is_newest_first_and_remains_after_invalid_submission(self):
        older = Quote.objects.create(
            weight=Decimal("3"),
            postcode="SW1A 1AA",
            delivery_type="standard",
            cost=Decimal("6"),
        )
        newer = Quote.objects.create(
            weight=Decimal("3"),
            postcode="EH1 1YZ",
            delivery_type="express",
            cost=Decimal("25"),
        )
        for response in [
            self.client.get(reverse("home")),
            self.client.post(reverse("home"), {"weight": "-1"}),
        ]:
            self.assertEqual(list(response.context["quotes"]), [newer, older])
            self.assertContains(response, "£6.00")
            self.assertContains(response, "£25.00")
            html = response.content.decode()
            self.assertLess(html.index("EH1 1YZ"), html.index("SW1A 1AA"))

    def test_valid_quotes_are_saved_and_displayed(self):
        for delivery_type, expected in [("standard", "6.00"), ("express", "25.00")]:
            with self.subTest(delivery_type=delivery_type):
                response = self.client.post(
                    reverse("home"),
                    {
                        "weight": "3",
                        "postcode": "SW1A 1AA",
                        "delivery_type": delivery_type,
                    },
                    follow=True,
                )
                self.assertContains(response, f"£{expected}")
                quote = Quote.objects.first()
                assert quote is not None, "Submitting a valid form should save a quote."
                self.assertEqual(quote.cost, Decimal(expected))
        self.assertEqual(Quote.objects.count(), 2)
        self.client.get(reverse("home"))
        self.assertEqual(Quote.objects.count(), 2)

    def test_invalid_input_does_not_save(self):
        for changes in [
            {"weight": "-1"},
            {"delivery_type": "unknown"},
            {"postcode": ""},
        ]:
            with self.subTest(changes=changes):
                response = self.client.post(
                    reverse("home"),
                    {
                        "weight": "3",
                        "postcode": "SW1A 1AA",
                        "delivery_type": "standard",
                        **changes,
                    },
                )
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
        self.assertEqual(Quote.objects.count(), 0)
