from django.contrib import admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "postcode", "weight", "delivery_type", "cost", "created_at")
    list_filter = ("delivery_type",)
    search_fields = ("postcode",)
    readonly_fields = ("created_at",)
